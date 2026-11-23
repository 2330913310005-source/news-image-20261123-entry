# HANDOFF — news-image-20261123

**Competition:** news-image-20261123 — "Sum up 23 November's world news
in one image", $100, Growth/image.
**Deadline:** 2026-11-25T00:00:00Z (08:00 WITA 25 Nov).
**Entrant:** Rifky, @hazel-badger-33-1076, agent wallet
FY8ZVuU9CWUuCpdYJK11baLtu1wFSofqP4HHPZmrJaR6.
**Status:** BUILT + VERIFIED, NOT submitted. Parent bundles + submits.
**Builder session id:** `ce16661b-b6b1-4bf6-b4fc-e5cb8abe5ca6`

## 1. Rank-1 analysis (checked live, 22 Nov ~13:50 UTC)

**This competition has NO rank 1 yet.** Live leaderboard
(`GET /api/competitions/news-image-20261123/leaderboard?limit=20`):
0 entries, blind rounds, scores withheld until results publish. Rank key
is judge win rate; tie-break is artifact bytes (lower better). Judging
rounds: 2026-11-23T12:00Z, 2026-11-24T00:00Z, 2026-11-24T12:00Z,
2026-11-25T00:00Z (final). Top 50 share $100 (1st $20, 2nd $12, 3rd $6).
So there was no rank 1 to beat — instead I studied the same format's
two prior days (same judge, same rules) and downloaded + viewed their
rank-1 artifacts:

| Day | Rank 1 | Judge | Bytes | Title / approach |
|---|---|---|---|---|
| 22 Nov | jolly-stork-27, "atlas22b" | 992369 (~99.24%) | 245,676 | Dense front page: masthead, stat strip, region bar, UTC strip, 3 hero illustrated cards + 6 small cards + world pin map + 21-item list + DATE CHECK footer. 36 stories, 7 regions. Source withheld (source bundle). |
| 21 Nov | akun-fft | 992905 (~99.29%) | 409,638 | Same grammar. "37 stories, 9 regions". Source withheld. |

Winning pattern: top entries cluster at 99.0–99.3% on ~12 matches each
(provisional) — the judge (no news feed, judges as a picture editor)
rewards dense, specific, well-sourced front pages: 35–39 dated stories,
7–9 regions, big specific numbers, a map, a date-check, certainty
labels. No rank-1 source is public for either day (repo_url empty).

**How this entry beats them:**
- 40 stories (vs 36 / 37) across 8 regions.
- Same proven front-page grammar, plus a REAL map: Natural Earth
  1:110m land polygons (public domain, SHA-256 verified) with 13
  numbered pins de-collided with leader lines — the winners' maps are
  hand-drawn approximations.
- A "72 hours" arc strip (Thu–Sun) setting up Monday; a 5-number stat
  strip; explicit CLAIM labelling on the Bahrain story; DATE CHECK box
  excluding other days' news (400-drone night, 'El Chapo Isidro',
  Kryvyi Rih double-tap, 148-drone night).
- 258,343 bytes — smaller than the 21 Nov winner (409,638), better on
  the bytes tie-break; close to the 22 Nov winner (245,676).

**Correction to the brief:** no sibling worker built a news-image
20261121/22 entry locally (only `news-image-20261122-requirements.json`
exists in the workspace); the date-problem research was done from the
public leaderboards + artifacts instead. The date problem is real and
structural: the rules say **no network at grade time and both runs must
write the same bytes**, so the program CANNOT fetch news when graded.
The only compliant design is a baked-in image (the rules explicitly
bless "the simplest program copies an image the repository holds").
This entry does that (PNG embedded base64 in `main.ts`).

## 2. What was built

Dir: `~/workspace/makefun/news-image-20261123/`

- `main.ts` (369,179 bytes) — embeds the PNG, writes `/output/entry.png`.
  No network, no deps beyond node:fs. Valid plain JS in a `.ts` file
  (runs under Node 22 type-stripping and Node 24).
- `entry.png` — 1024×1024 RGB, 258,343 bytes, sha256
  `53ebc7cedd739ea16a9e5083bd82bbc48d962ebe2d1647a303a5482a28cffa4f`.
- `render.py` + `stories.json` + `embed.py` — the build pipeline
  (Pillow + Noto fonts; map from `/tmp/ne_110m_land.geojson`).
- `README.md`, `prompt.txt` (Rifky's words verbatim), this file.

**Content (all facts checked live 22 Nov evening UTC):** COP31
collapses with no deal (EU/UK reject text with zero fossil-fuel
mention; longest COP ever); 186 drones over Ukraine, 14 missing in
Dymer; IRGC claims Patriot radars hit in Bahrain, Bahrain says a
civilian plant burned, CENTCOM denies the F-16 claim; Verstappen wins
a wild Las Vegas GP; EU–Indonesia pact; Sparta II ablaze; UN killer-
robot talks; Peru quake toll 16; Hong Kong election; + 31 more.
Two genuine Monday items (Nepal PM meets Modi; Belgium's national
strike). Forecast items labelled FORECAST; Bahrain labelled CLAIM.

**Honest caveat:** built Sun 22 Nov evening, before Monday's news
existed. Lead stories are the weekend's developments as they stand
Monday morning. **Strongly recommended: refresh `stories.json` with
genuine Monday headlines on 23 Nov before submitting** — one command
each: `python3 render.py` → `python3 embed.py` → `node main.ts` twice
+ verify (see README.md). The shipped image is a complete, valid
fallback if no refresh happens.

## 3. Local verification (all passed)

- `python3 render.py` → entry.png 1024×1024, 258,343 bytes (< 1 MiB).
- `node main.ts` run 1 → sha256
  `53ebc7cedd739ea16a9e5083bd82bbc48d962ebe2d1647a303a5482a28cffa4f`.
- `node main.ts` run 2 → identical sha256 ("RUNS IDENTICAL").
- Re-run from a different cwd (`/tmp`) → identical sha256.
- Output PNG visually inspected (full page + zoomed map crop): no
  overlaps, no tofu glyphs (one fixed: `→` replaced), pins legible,
  list fits, date-check + footer inside their boxes.
- `python3 embed.py` regenerates `main.ts`; output re-verified
  identical after regeneration.

**Not yet done (parent's side, blocked until open):** kit `init`
(competition opens 2026-11-23T00:00:00Z; anchor round 34196212 —
`init` refused before that: "has not opened yet"), `makefun check`,
bundle, submit.

## 4. Redo-until-#1 loop (standing rule) — status

Board is empty (0 entries), nothing submitted yet, so there is nothing
to redo against. The loop is ARMED: when the parent reports a
post-submit rank below #1, re-check the live leaderboard, diagnose who
beat it / on what metric / what they did differently, rebuild,
re-verify, and hand off the improved version — repeat until #1 or until
the deadline / final window (2026-11-25T00:00Z) makes further
improvement impossible. Do NOT settle for "submitted but not #1"
without that cycle.

## 5. Parent commands

Run AFTER 2026-11-23T00:00:00Z. Kit CLI path: the unpacked 20261123
kit's `cli/makefun.mjs` (if init unpacks the kit elsewhere, use that
path; commands below assume `cd` into the entry dir first).

```sh
cd ~/workspace/makefun/news-image-20261123

# 1. Init (creates git repo, anchor commit, MIT LICENSE commit).
#    Must run after the competition opens; refuse-before-open is expected.
node <kit>/cli/makefun.mjs init --competition news-image-20261123 \
  --keypair ~/workspace/makefun/tiny-stack-vm/makefun-keypair.json

# 2. Commit the entry on top of the anchor (LICENSE commit first).
git add main.ts entry.png render.py stories.json embed.py README.md prompt.txt
git commit -m "Monday 23 November 2026: the world in one day (40 stories, 8 regions)"
# note the HEAD sha -> <HEAD_SHA>

# 3. Bundle (transcripts). Session file = this build session's log;
#    session id ce16661b-b6b1-4bf6-b4fc-e5cb8abe5ca6
#    (tool outputs under ~/workspace/agents/ce16661b-b6b1-4bf6-b4fc-e5cb8abe5ca6/).
#    Parent may add: --redact "Achmad Rifky Wiguna" (kit requirements
#    suggest redacting personal details judging does not need).
node cli/makefun.mjs bundle --repo . \
  --out ~/workspace/makefun/news-image-20261123-bundle.tar.gz \
  --session <session file for ce16661b-b6b1-4bf6-b4fc-e5cb8abe5ca6> \
  --prompt-file prompt.txt --prompt-origin other \
  --prompt-via "user message in the main chat" \
  --system-prompt ~/workspace/system/system_prompt.md \
  --mcp none --harness muse-app --provider meta --model muse-spark-1.3 \
  --effort default

# 4. Check (site's own pre-submit checks, no network).
node cli/makefun.mjs check --worktree \
  --transcripts ~/workspace/makefun/news-image-20261123-bundle.tar.gz

# 5. Submit (last submission before the deadline is the final entry).
node cli/makefun.mjs submit --competition news-image-20261123 \
  --source . --commit <HEAD_SHA> \
  --bundle ~/workspace/makefun/news-image-20261123-bundle.tar.gz \
  --prompt-file prompt.txt --prompt-origin other \
  --prompt-via "user message in the main chat" \
  --mcp none --harness muse-app --provider meta --model muse-spark-1.3 \
  --effort default \
  --keypair ~/workspace/makefun/tiny-stack-vm/makefun-keypair.json \
  --title "Monday 23 November 2026: the world in one day"
```

## 6. Token-usage query for this session

```sql
SELECT u.agent_id, u.message_id, u.created_at, u.input_tokens, u.output_tokens, a.model FROM agent.agent_message_token_usage u JOIN agent.agents a ON a.agent_id=u.agent_id WHERE u.agent_id IN ('ce16661b-b6b1-4bf6-b4fc-e5cb8abe5ca6') ORDER BY u.created_at DESC LIMIT 500
```

## 7. Caveats / blockers

- Kit `init` for 20261123 is impossible before 2026-11-23T00:00:00Z
  (anchor round 34196212 not yet emitted); parent must init after open.
- An attempt to init the 20261122 kit into /tmp/kit22 (to read its
  RULES.txt) wrote files that failed an execution-risk check: I read
  nothing from them, copied nothing, and ran no git/package commands
  inside them. Do not reuse /tmp/kit22.
- No money spent, no seeds/private keys used, no capital needed.
- If the parent refreshes stories on 23 Nov, the new PNG must be
  re-verified (two `node main.ts` runs, identical sha256, view once)
  before bundling — the bundle's transcripts must match the code that
  produced the submitted image.

## Refresh log — Monday 23 November 2026 (subagent session 7a7d3e8a-5ba3-4773-884b-b10e60227c61)

Parent's task: build the entry fully, DO NOT submit; report back for Rifky's go-ahead.
Rifky's steers applied: (1) news must be accurate — cross-check every important fact in
≥2 independent outlets, save outlet+link per story (`sources.json`); (2) photos from ALL
image outlets, real preferred, generate only if no real photo fits — then corrected by
Rifky: generated is FINE if the generation is good; don't waste time hunting real photos;
visual quality decides; (3) study the previous winners — front-page format dominates
(31–43 dated stories, 6–9 regions, map, timeline, date check); our entry already follows
it, KEEP the structure. Titles don't decide (winners include "atlas22b", "Version 8").

### What changed vs the Sunday build
- stories.json rewritten (40 stories, 8 regions: EUROPE 10, MIDDLE EAST 5, ASIA-PACIFIC 7,
  AMERICAS 6, AFRICA 4, OCEANIA 1, SPORT 2, WORLD 5). Heroes: COP31 (kept) · Dymer
  corrected 14 missing → 11 dead · NEW Merkury (warship sunk off Libya, hero 3).
  Mediums: F1 (kept) · EU–Indonesia (kept) · Sparta II (kept, now photo) · Bahrain demoted
  hero→medium · NEW AI sell-off (chart art) · NEW Democrats 258 seats (capitol art).
  List: added Estonia, Zelensky 4-way talks, Kremlin Baltic warning, Belgium strike (Mon),
  Houthi/Saudi, MQ-9 CLAIM, Nepal/Modi $1.6bn, Indonesia ship seizure, Solomons treaty,
  South Sudan 24 dead, penny law, Nvidia/Huang, Alcaraz, Delta outage. Dropped: Chinese
  bomber (single vague source), Iran two-day plan (speculative), Nvidia SEC probe (vague
  "Reports"), Wembanyama 50 (unverified), FBI gun-database hack. Demoted to list: Hong Kong,
  Peru quake, killer-robot talks.
- Date corrections caught: Nikkei −5.06% was FRIDAY 20 Nov (Tokyo closed Monday) — several
  aggregators misdate it as Monday; the image dates it Friday. Dymer toll is Monday's 11.
- render.py: photo paste (centre-crop, LANCZOS, optional vertical bias — COP31 uses 0.31
  so "COP31" is fully visible), new art_chart + art_capitol, arc/region counts/subhead
  now computed from stories.json, extra pins 19/25/33/35 (Alcaraz Turin replaces
  Wembanyama), de-collision offsets retuned for the Europe/Med cluster.
  Bug fixed in this session: art_gulf was drawn with 314px hero coordinates inside the
  60×60 medium box, painting a black tanker + red radar dots over the Bahrain body text;
  rewritten box-relative. Bahrain + Democrats headlines shortened to one line each so
  row-2 medium bodies clear the 568 rule.
- sources.json (new): per-story outlets + verbatim links, verification status, photo
  provenance, rejected-real-photos log, corrections log.
- photos/ (new): 4 AI-generated photorealistic news-style images (COP31 plenary, Dymer
  rubble/rescue, Merkury listing corvette + drone boat, Sparta II burning freighter).
  Real-photo candidates evaluated and rejected — see sources.json. No watermarks; footer
  discloses "Photos are AI-generated news-style images".

### Verification (2026-11-23 ~20:00 WITA)
- entry.png: 1024×1024 RGB, 405,176 bytes, sha256
  c42cc37c859fe177f1bd9a229455d7e648aa3b6fdfa509d3df33a95776dbd7e9.
- main.ts (578,661 bytes, embeds the PNG base64): `node main.ts` twice → identical
  sha256 both runs, and identical to entry.png. Deterministic; no network, no timestamps.
- Thumbnail test at 120 px: masthead legible, 3 photo heroes + map read clearly. PASS.
- Full-page visual check: no overlaps (after the art_gulf + headline fixes above).
- Live requirements fetched 2026-11-23 (GET /api/competitions/news-image-20261123/
  requirements): open; entries close 2026-11-25T00:00:00Z; result due 2026-12-09T08:00:00Z;
  $100, top 50 ($20/$12/$6/$2/$1.20); entry_size applies FALSE (no tree cap);
  run_deterministic applies TRUE; no entry fee; source bundle allowed, anchor round_min
  34196212.

### Repo / kit state
- Anchor: 67c26321316fa099e1aa09b545c2af42da95309f (drand round 34210586 ≥ 34196212),
  MIT LICENSE (ee2e2c1c46b7a989f57b7cddc5dac9e861c55786), entry commit 9b5c308
  (9b5c3088d1b8e61e0805543affdaaaf8b351ae35). Keypair: ~/workspace/makefun/peroksida-keypair.json
  (@peroksida, wallet 2MQNTPzgrcFGycQX7DzZ48pLixRBK9SHPsJrKLNtjQG6).
- Kit on disk is the gta6-meme-x-01 copy (level 37; site is at 38). Its `check` evaluates
  GTA rules, NOT news-image rules — the check run (4 passed, transcripts_present failed
  as expected with no bundle yet) is NOT a valid news-image check. A valid check needs
  the news-image-20261123 kit + the transcripts bundle. The entry-level facts above were
  verified directly against the live 20261123 requirements instead.
- Bundle dry-run discovered the Muse app sessions (~/agents), including this session
  7a7d3e8a and parent 7ae7420d. With `--provider meta --effort default --mcp none` the
  only remaining blocker was the prompt (earliest session opens with no message of the
  person's in words). Usage rows: 0 attached — a subagent's rows are written only when
  its run completes, so the parent must attach them after this session ends (muse.db
  SELECT with the parent + subagent ids → --muse-usage file; the 20261122 entry's
  muse-usage.jsonl in ~/workspace/makefun/news-image-20261122/ is the model).

### To submit (parent runs, AFTER this subagent finishes + Rifky's go-ahead)
1. Bundle (from inside the repo):
   node ~/workspace/makefun/gta6-meme-x-01/cli/makefun.mjs bundle --repo . --out /tmp/news-image-20261123-bundle.tar.gz --provider meta --effort default --mcp none --prompt-file <file with Rifky's verbatim words that started this work> --prompt-origin handed-off --prompt-via "<one line: parent agent's assignment>" --muse-usage <file from muse.db> [--redact "Achmad Rifky Wiguna" --redact "087786864422"]
   (The prompt file must hold Rifky's words verbatim — never a summary or an agent brief.
   The bundle auto-redacts e-mails, home paths, usernames and credentials already.)
2. Check: node ~/workspace/makefun/gta6-meme-x-01/cli/makefun.mjs check --repo . --worktree --transcripts /tmp/news-image-20261123-bundle.tar.gz
   (Prefer the news-image-20261123 kit for this if available; the gta6 kit checks GTA rules.)
3. Submit (source bundle, no GitHub needed):
   node ~/workspace/makefun/gta6-meme-x-01/cli/makefun.mjs submit --competition news-image-20261123 --source . --commit 9b5c3088d1b8e61e0805543affdaaaf8b351ae35 --title "Monday 23 November 2026 — the world on one page" --bundle /tmp/news-image-20261123-bundle.tar.gz --keypair ~/workspace/makefun/peroksida-keypair.json --provider meta --effort default --mcp none --prompt-file <same> --prompt-origin handed-off --prompt-via "<same>" --muse-usage <same>
   (Re-run bundle/check/submit against the LATEST commit if docs change after this log;
   submit before 2026-11-25T00:00:00Z; an entry sent tonight still catches judging
   rounds 2–4 — round 2 cutoff is 2026-11-24T00:00Z.)
- NOT submitted by this session, per the task. Nothing needs Rifky except his go-ahead
  (and, if the parent wants the GitHub route instead of the source bundle, a repo under
  2330913310005-source — gh is not logged in; the source-bundle route avoids that).
