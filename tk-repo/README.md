# tuzwa-toolkit

Byte-exact copy of the Backend batch toolkit of the claude.ai project "Backend-DFS-Tuzwa Guncel" (2026-09-15).

Layout on disk = layout the session-start copy used to produce in /home/claude/work/:

- `toolkit/`  — every `./X` line of `toolkit/MANIFEST.md` (scripts + spec docs)
- `rules/`    — every `./rules/X` line of the manifest (rule docs)
- `title-check.py`, `desc-check.py`, `usage-efficiency-runbook.md` — root, as before

NOT in this repo (the repo is public): `toolkit/shopify-api-credentials.md` and
`rules/dataforseo-credentials.md`. Those two stay project docs and are read with `project_read`.

Session start (replaces the copy agent):

    git clone --depth 1 https://github.com/AysegulSu/tuzwa-toolkit.git /home/claude/work
    cd /home/claude/work && sha256sum -c MANIFEST.sha256 --quiet && echo TOOLKIT OK

Keep in sync: when a toolkit or rule doc changes in the project, change it here too (same turn), and
refresh its line in `toolkit/MANIFEST.md` as before.
