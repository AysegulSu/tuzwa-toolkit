# Keyword word-order variants — measured in separate DataForSEO calls (user decision 2026-09-11)

**Finding (ddl2-batch1 p00, product 11212354748452).** The title dropped `noise cancelling headphones`
(165,000, the highest fitting keyword and the old title's own opener) as "low volume". Reproduced: Google Ads
folds keywords that are the same words in a different order into ONE close variant when they arrive in the
same request, and reports the low variant's volume for both.

| sent | `noise cancelling headphones` returns |
|---|---|
| alone | 165,000 |
| in the same request as `headphones noise cancelling` | 2,400 |

Measured alone, the two orders are different keywords (`headphones noise cancelling` 2,400; `vintage table lamp`
3,600 vs `lamp table vintage` 2,900). The pair is routine in this pipeline: `source_windows.py` emits the supplier
title's order, the extraction agent's candidates give the natural order.

**Rule.** `kw_measure.py` buckets the todo list by sorted word bag and sends the members of one bag in separate
ROUNDS (round 0 = first member of every bag, round 1 = second, …); each round is chunked and called on its own.
Both variants are still measured, each with its own volume; the title step picks the higher one. Cost: one extra
call (~$0.09) per round beyond the first. The stderr line `… in N call(s) over R round(s) — V word-order
variant(s) moved to later rounds` and the `[order variant, own call]` lines go into the run log.

**Do not** "dedupe to one variant" instead — the reversed form can be the lower one, and dropping the natural
form loses the real volume.

**Open question, not handled:** Google may also fold plural / singular (`headphone` vs `headphones`) the same
way. Not reproduced yet; check when a plural pair looks suspiciously equal in a cache.

**Earlier batches.** Any kw-cache produced before 2026-09-11 can carry this error silently: a keyword whose
reversed order was also in the list may hold the reversed form's small volume. Audit = bucket the cache by sorted
word bag, re-measure every bag with 2+ members in separate calls, compare.
