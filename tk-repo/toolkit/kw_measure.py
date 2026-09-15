#!/usr/bin/env python3
"""kw_measure.py — the ONE path from a candidate list to DataForSEO and into kw.txt (README step 4 and step 1b).

Added 2026-09-09 (user decision) after the 40501 errors of 2026-09-09 07:50 / 08:18 UTC in the DataForSEO error log.
`google_ads/search_volume/live` rejects a keyword over 80 characters or 10 words (`40501 Invalid Field: 'keywords'.
Keyword text exceeds the allowed limit`) and ONE such keyword voids the WHOLE task: the call returns a top-level
`20000 Ok` with zero results, which reads as a successful call, and every keyword of that chunk is then either
re-sent by hand or left without a volume. source_windows.py has dropped its own over-limit windows since
2026-09-08, but the extraction agents' candidates/cNN.json and the step-1b extra list went to the API unfiltered —
the two keywords in the 2026-09-09 log were whole supplier titles (14 and 17 words) from that side. Until now step 4
was an ad hoc curl, so the filter had no fixed place to live. This script is that place.

  python3 kw_measure.py --kw kw.txt candidates/*.json candidates/source_windows.txt [more.txt ...]
                        [--creds rules/dataforseo-credentials.md] [--cache /mnt/user-data/outputs/kw-cache-<tag>.md]
                        [--chunk 950] [--dry-run]

Inputs: any number of .json (a list of strings, or any JSON whose string leaves are keywords — cNN.json in every shape
the extraction agents have produced) and .txt (one keyword per line) files. Everything is unioned, normalised the way
source_windows.norm() normalises a title (lowercase, apostrophes and other non [a-z0-9 ] characters removed —
DataForSEO rejects them too), deduped, and keywords already in kw.txt are skipped, so a re-run costs nothing.

Three guards, in order:
  1. measurable() from source_windows.py — over 80 characters / 10 words is dropped BEFORE chunking, whatever file it
     came from; each dropped phrase is named on stderr. Nothing measurable is lost: such a phrase is a whole supplier
     title and its 2–4-word windows are already candidates.
  2. Every task's status_code must be 20000 — a 40501 (invalid keyword), a 40202 (rate limit) or any other code is
     printed with its message and the run EXITS 1; nothing is written for that chunk.
  3. A chunk that comes back with ZERO results is a hard error (exit 1), never a set of zero volumes — this is the
     silent-void case of batch4 and 2026-09-09. A keyword the API did not echo back at all is recorded at 0 and counted
     on stderr as "not returned", so the count is visible in the run log.
  Plus two shape/pace guards from the 2026-09-08 error log (100 rows read on 2026-09-09): a toolkit script's own stderr
  report line captured into a candidates file (`2>&1`) is refused as a keyword (REPORT_RE — after normalisation such a
  line can be exactly 10 words and would pass guard 1), and calls are paced 6 s apart with ONE retry after 65 s on a
  4020x (rate limit) or 5xxxx (DataForSEO server-side, e.g. 50301) answer, never a loop — the account's live limit is 12 calls/min and a retry loop produced ~90 40202 rows.

Word-order guard (added 2026-09-11, user decision — ddl2-batch1 p00): Google Ads folds keywords that are the same
words in a different order ("noise cancelling headphones" / "headphones noise cancelling") into ONE close variant when
they arrive in the SAME request, and then reports the low variant's volume for both — measured alone they are
different keywords (165,000 vs 2,400; `vintage table lamp` 3,600 vs `lamp table vintage` 2,900). source_windows.py
makes such pairs routine: the supplier title's order gives one variant, the extraction agent's candidate list gives the
natural one. So the todo list is bucketed by its sorted word bag and the members of one bag are spread over separate
ROUNDS: round 0 holds the first member of every bag, round 1 the second, and so on; each round is chunked and sent on
its own, so two order-variants never share a request. Cost: one extra call per round beyond the first (a batch usually
has a few dozen second-members, i.e. one ~$0.09 call). The round count is printed on stderr and belongs in the run log.

Proxy backoff (added 2026-09-11, user decision): the sandbox egress proxy intermittently answers 403 to CONNECT for
~20 s and then recovers (seen on the Shopify host the same day; api.dataforseo.com goes through the same proxy).
With urllib such a refusal surfaces as URLError("Tunnel connection failed: 403"), not HTTPError, and used to crash
the run. post() now retries a transport-level failure (URLError, socket timeout — NOT an HTTPError from DataForSEO
itself) after 5, 10, 20, 40 s. This is separate from, and does not touch, the single 65 s retry on a 4020x/5xxxx task
status above. A call that succeeds first time never enters this path — zero cost when the proxy is healthy.

Writes: kw.txt gets `keyword|volume|competition|cpc` appended after EACH successful chunk (a crash keeps the earlier
chunks; the re-run measures only what is missing); --cache appends the same lines to the kw-cache doc. --dry-run
prints the counts and the dropped phrases, calls nothing, costs nothing. Cost: ~$0.09 per 950-keyword chunk.
"""
import argparse, base64, json, os, re, sys, time, urllib.request, urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from source_windows import measurable, norm, MAX_CHARS, MAX_WORDS  # the one definition of the limit

URL = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"
LOCATION, LANGUAGE = 2840, "en"          # US, English — title-format-rule.md §1
DEFAULT_CHUNK = 950                       # API max is 1,000; README step 4 uses 950
RETRY_SLEEP = 65                          # seconds — a 4020x rate-limit answer is retried once after the minute turns
CALL_GAP = 6                              # seconds between calls: this account's live limit is 12 calls/min ("12 >= 12" in the
                                          # 2026-09-08 log, ~90 errors from a tight retry loop) — 6 s keeps a run at <= 10/min
TUNNEL_BACKOFF = (5, 10, 20, 40)          # seconds between retries of a proxy CONNECT 403 / transport error (see docstring)


def load_creds(path):
    """Login/password from dataforseo-credentials.md — read, never printed."""
    login = pw = None
    for line in open(path, encoding="utf-8"):
        m = re.match(r"- Login: `(.*)`", line)
        if m:
            login = m.group(1)
        m = re.match(r"- Password: `(.*)`", line)
        if m:
            pw = m.group(1)
    if not login or not pw:
        sys.exit(f"kw_measure: no login/password found in {path}")
    return login, pw


def strings_of(obj):
    """Every string leaf of a JSON value — cNN.json has had several shapes; all of them are covered by this."""
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, list):
        for x in obj:
            yield from strings_of(x)
    elif isinstance(obj, dict):
        for x in obj.values():
            yield from strings_of(x)


# A toolkit script's OWN report line, captured into a candidates file with `2>&1` — on 2026-09-08 09:33 UTC the line
# `source windows 50 titles - 1253 windows 1253 not yet measured` went to the API four times (40501 "too many words");
# after normalisation it is 10 words and would pass the length gate, so it is refused by shape, not by length.
REPORT_RE = re.compile(r"^\s*(source_windows|kw_measure)\s*:|^\s*\[(oversize|not returned)\]|"
                       r"\btitles?\s*(->|-)\s*\d+\s+windows\b|\bnot yet measured\b|\bdropped over the dataforseo\b", re.I)


def read_candidates(paths):
    raw, reports = [], []
    for p in paths:
        if p.endswith(".json"):
            items = list(strings_of(json.load(open(p, encoding="utf-8"))))
        else:
            items = [line.strip() for line in open(p, encoding="utf-8")]
        for s in items:
            (reports if REPORT_RE.search(s) else raw).append(s)
    for s in reports:
        sys.stderr.write(f"  [report line, not a keyword] {s[:90]}\n")
    return raw


def clean(kw):
    """Normalise as source_windows does a title, apostrophes closed up first (kid's -> kids, not kid s);
    '' when nothing measurable is left."""
    return " ".join(norm(re.sub(r"[’']", "", kw)))


def known_keywords(kw_path):
    known = set()
    if os.path.exists(kw_path):
        for line in open(kw_path, encoding="utf-8"):
            if "|" in line:
                known.add(line.split("|", 1)[0].strip().lower())
    return known


def post(auth, keywords):
    body = json.dumps([{"location_code": LOCATION, "language_code": LANGUAGE,
                        "search_partners": False, "keywords": keywords}]).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type": "application/json", "Authorization": "Basic " + auth})
    # Transport-level retry only (proxy CONNECT 403, reset, timeout). An HTTPError is DataForSEO's own answer and is
    # raised through unchanged — the caller decides. Nothing is repeated if the first attempt gets through.
    for i, wait in enumerate(TUNNEL_BACKOFF + (None,)):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except urllib.error.HTTPError:
            raise
        except (urllib.error.URLError, OSError) as e:
            if wait is None:
                sys.exit(f"kw_measure: transport error after {len(TUNNEL_BACKOFF)} retries: {e}")
            sys.stderr.write(f"kw_measure: transport error ({e}) — retry {i + 1}/{len(TUNNEL_BACKOFF)} in {wait}s\n")
            time.sleep(wait)


def check_response(resp, n_sent, label):
    """Guards 2 and 3. Returns the result list or exits 1 with the reason. Never returns an empty list."""
    if resp.get("status_code") != 20000:
        sys.exit(f"kw_measure: {label}: API status {resp.get('status_code')} {resp.get('status_message')}")
    tasks = resp.get("tasks") or []
    if len(tasks) != 1:
        sys.exit(f"kw_measure: {label}: expected 1 task, got {len(tasks)}")
    t = tasks[0]
    if t.get("status_code") != 20000:
        # 40501 = invalid keyword (this script's reason for existing); 4020x = rate limit; anything else = report.
        sys.exit(f"kw_measure: {label}: task status {t.get('status_code')} {t.get('status_message')} "
                 f"— nothing written for this chunk")
    result = t.get("result") or []
    if not result:
        sys.exit(f"kw_measure: {label}: task 20000 Ok but ZERO results for {n_sent} keywords — the chunk was voided "
                 f"(an invalid keyword got through?). Nothing written; fix the list and re-run.")
    return result


def bag(kw):
    """Sorted-word key: every word-order variant of a phrase maps to the same key."""
    return " ".join(sorted(kw.split()))


def rounds_of(todo):
    """Spread word-order variants over separate rounds so no two of them share one API request.
    Returns a list of lists; round r holds the r-th member (in input order) of every bag."""
    groups = {}
    for k in todo:
        groups.setdefault(bag(k), []).append(k)
    rounds = []
    for members in groups.values():
        for r, k in enumerate(members):
            while len(rounds) <= r:
                rounds.append([])
            rounds[r].append(k)
    return [sorted(rd) for rd in rounds]


def fmt(row):
    vol = row.get("search_volume")
    comp = row.get("competition") or "NONE"
    cpc = row.get("cpc")
    return f"{row['keyword'].lower()}|{0 if vol is None else int(vol)}|{comp}|{0 if cpc is None else cpc}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+", help="candidate files: .json (string leaves) and/or .txt (one per line)")
    ap.add_argument("--kw", default="kw.txt", help="kw.txt to read (skip known) and append to")
    ap.add_argument("--creds", default=None, help="dataforseo-credentials.md (default: rules/ or . next to this script)")
    ap.add_argument("--cache", default=None, help="kw-cache-<tag>.md to append the same lines to")
    ap.add_argument("--chunk", type=int, default=DEFAULT_CHUNK)
    ap.add_argument("--dry-run", action="store_true", help="count and list drops; no API call")
    a = ap.parse_args()
    if a.chunk < 1 or a.chunk > 1000:
        sys.exit("kw_measure: --chunk must be 1..1000")

    raw = read_candidates(a.inputs)
    known = known_keywords(a.kw)
    cleaned, empty, dropped, todo = 0, 0, [], []
    seen = set()
    for kw in raw:
        c = clean(kw)
        if not c:
            empty += 1
            continue
        if c != kw.strip().lower():
            cleaned += 1
        if c in seen:
            continue
        seen.add(c)
        if not measurable(c):                       # guard 1
            dropped.append(c)
            continue
        if c in known:
            continue
        todo.append(c)
    todo.sort()
    rounds = rounds_of(todo)                            # word-order guard — see the module docstring
    chunks = [(r, rd[i:i + a.chunk]) for r, rd in enumerate(rounds) for i in range(0, len(rd), a.chunk)]
    n_variants = sum(len(rd) for rd in rounds[1:])

    sys.stderr.write(
        f"kw_measure: {len(raw)} raw -> {len(seen)} unique ({cleaned} normalised, {empty} empty), "
        f"{len(dropped)} dropped over the DataForSEO limit ({MAX_CHARS} chars / {MAX_WORDS} words), "
        f"{len(known)} already in {a.kw}, {len(todo)} to measure in {len(chunks)} call(s) over "
        f"{len(rounds)} round(s) — {n_variants} word-order variant(s) moved to later rounds\n")
    for rd in rounds[1:]:
        for k in rd:
            sys.stderr.write(f"  [order variant, own call] {k}\n")
    for c in dropped:
        sys.stderr.write(f"  [oversize] {len(c)}c {len(c.split())}w  {c[:70]}…\n")
    if a.dry_run or not todo:
        return

    creds = a.creds
    if creds is None:
        here = os.path.dirname(os.path.abspath(__file__))
        for cand in (os.path.join(here, "rules", "dataforseo-credentials.md"),
                     os.path.join(here, "dataforseo-credentials.md"), "rules/dataforseo-credentials.md"):
            if os.path.exists(cand):
                creds = cand
                break
        if creds is None:
            sys.exit("kw_measure: --creds not given and dataforseo-credentials.md not found")
    login, pw = load_creds(creds)
    auth = base64.b64encode(f"{login}:{pw}".encode()).decode()

    total_written, total_not_returned = 0, 0
    for ci, (rnd, chunk) in enumerate(chunks):
        label = f"chunk {ci + 1}/{len(chunks)} round {rnd} ({len(chunk)} keywords)"
        assert all(measurable(k) for k in chunk)          # the invariant this script exists for
        assert len({bag(k) for k in chunk}) == len(chunk)  # word-order guard: no two variants in one request
        try:
            resp = post(auth, chunk)
        except urllib.error.HTTPError as e:
            sys.exit(f"kw_measure: {label}: HTTP {e.code} {e.reason}")
        # ONE retry, after the minute turns, on a rate-limit answer (4020x — this account: 12 calls/min) or a DataForSEO
        # server-side error (5xxxx, e.g. 50301 Internal Error — 3 rows in the 2026-09-08 log). Never a loop.
        t0 = (resp.get("tasks") or [{}])[0]
        code0 = str(t0.get("status_code", ""))
        if resp.get("status_code") == 20000 and (code0.startswith("4020") or code0.startswith("5")):
            sys.stderr.write(f"kw_measure: {label}: {t0.get('status_code')} {t0.get('status_message')} — "
                             f"retrying once in {RETRY_SLEEP}s\n")
            time.sleep(RETRY_SLEEP)
            resp = post(auth, chunk)
        result = check_response(resp, len(chunk), label)  # guards 2 and 3

        by_kw = {r["keyword"].lower(): r for r in result if r.get("keyword")}
        lines, not_returned = [], []
        for k in chunk:
            if k in by_kw:
                lines.append(fmt(by_kw[k]))
            else:
                not_returned.append(k)
                lines.append(f"{k}|0|NONE|0")
        with open(a.kw, "a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        if a.cache:
            with open(a.cache, "a", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
        total_written += len(lines)
        total_not_returned += len(not_returned)
        with_vol = sum(1 for r in result if r.get("search_volume"))
        sys.stderr.write(f"kw_measure: {label}: {len(result)} results, {with_vol} with volume, "
                         f"{len(not_returned)} not returned (recorded at 0), cost "
                         f"{(resp.get('tasks') or [{}])[0].get('cost', '?')}\n")
        for k in not_returned:
            sys.stderr.write(f"  [not returned] {k}\n")
        if ci + 1 < len(chunks):
            time.sleep(CALL_GAP)
    sys.stderr.write(f"kw_measure: done — {total_written} lines appended to {a.kw}, "
                     f"{total_not_returned} not returned, {len(dropped)} dropped oversize\n")


if __name__ == "__main__":
    main()
