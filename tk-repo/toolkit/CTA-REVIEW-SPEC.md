# CTA-REVIEW-SPEC — the independent CTA reader (one Sonnet agent per batch; added 2026-09-06, user decision after blr-batch26)

Purpose: a second, independent reading of the 3 × N CTA lines by an agent that did NOT write the descriptions and does
not see them — only each product's source facts and its three CTA lines. In blr-batch26 eight feature-count / audience
lines passed cta_check.py and the main-context 6c reading and were caught only by the user (p45, p47). This agent marks;
it never rewrites. Cost: ~0.1M tokens per 50 products. Runs in README step 6c, after the main-context CTA pass, before payloads.

## Inputs (working dir /home/claude/work)
- rules/cta-benefits-metafield.md — read IN FULL, especially "HANGİ 3 BENEFIT" and "Gerçek örnekler — blr-batch26".
- cta_review_input.json — written by the main context: `[{"idx": NN, "product": "<identity line>", "facts": [...], "specs": [...], "cta": ["icon|text", ×3]}]`. No description text, no title.

## What to mark — CERTAIN failures only (user decision: no borderline flags)
Mark a line ONLY when it clearly is one of these:
1. A count or list of features — "Seven colors, one remote", "Six modes for every need", "3 heat settings", "with remote".
2. A description of what the product IS or DOES with no problem solved — "Looks and sounds like a predator", "Lifelike fur
   and details", "Adjustable brightness", "Works with a remote control".
3. An audience or occasion line with no problem — "Great for any age", "Great gift for any age", "Perfect for travel".
4. A variant fact — sizes, colours, pack counts.
5. An outcome the source does not state (medical / physiological / "for good" / "years").
6. A line whose payoff is not traceable to the facts/specs given.

Do NOT mark: a runtime, capacity or time figure attached to a result ("Up to 40 hours per charge", "Runs 3-8 hrs per
charge", "Warm in under 30 seconds", "Weeks between charges") — the rule allows numeric proof of a result; a line you
merely "would have written differently"; length or icon choices (the script measures those).
The test for every line: can it be read as "that problem is gone / you no longer have to …"? If yes, or if you are not
sure, do not mark it.

## Output — cta_review.json and nothing else in the reply
`[{"idx": NN, "line": "<the CTA text verbatim>", "reason": "<one of the six categories above, ≤12 words>",
   "suggest": "<a ≤30-char benefit line from the SAME facts, or empty>"}]` — one entry per marked line; `[]` when none.
Reply to the main context with ONLY: `cta-review: N lines marked on M products` and the list `NN | line | reason`.

## Main-context part (README 6c)
Read every marked line against the rule yourself; a real miss goes back to that product's description agent with the
6b/6c message (one message per agent, README 6d); a wrong mark is dismissed with no action. The run log carries:
`CTA independent review: N marked, K confirmed and corrected (pNN …), N-K dismissed` — a log without this line means the
step was skipped. Never use Haiku for this agent.
