# Monday 23 November 2026 — the world in one day

make.fun entry for **news-image-20261123** ($100, Growth/image).
A program that writes one image to `/output/entry.png`: a newspaper
front page summing up Monday 23 November 2026 in 40 dated stories
across 8 regions.

## Files

- `main.ts` — the entry. Embeds the finished PNG (base64) and writes it
  to `/output/entry.png`. No network, fully deterministic: every run
  writes identical bytes.
- `entry.png` — the front page, 1024×1024, 258,343 bytes (limit 1 MiB).
- `render.py` — builds `entry.png` from `stories.json` (Pillow + Noto
  fonts; map from Natural Earth 1:110m land polygons, public domain).
- `stories.json` — all 40 stories, stats, region counts, date-check text.
- `embed.py` — regenerates `main.ts` from `entry.png`.
- `prompt.txt` — Rifky's words for the submission.
- `HANDOFF.md` — rank-1 analysis, verification, submit commands.

## The image

Masthead + red subhead, 5-number stat strip (0 fossil-fuel mentions in
the COP31 text · 186 drones · 14 missing in Dymer · day 268 of the Iran
war · 35 lead changes in Las Vegas), region bar, a "72 hours" arc from
Thursday to Sunday night, 3 illustrated hero cards (COP31 collapses,
Dymer drone night, Bahrain radar strikes), 6 medium cards, a real world
map with 13 numbered pins, a 31-item list, a DATE CHECK box excluding
other days' news, and a certainty legend (REPORTED / CLAIM / FORECAST).

## Honesty note (read before submitting)

This image was built on Sunday 22 Nov evening UTC, before Monday's news
existed. Its lead stories are the weekend's developments as they stand
on Monday morning (COP31's collapse, the Dymer rescue, the Gulf
aftermath), plus two genuine Monday items (Nepal PM meets Modi;
Belgium's national strike). Every fact was checked against live
reporting (Reuters, AP, BBC, The Times, Al Jazeera, Xinhua, Formula 1).
Nothing is invented; forecast items are labelled FORECAST and the
Bahrain strike is labelled CLAIM (one side's account).

## Refresh before submitting (strongly recommended)

For the best odds, refresh with genuine Monday headlines on 23 Nov:

1. Edit `stories.json` (replace/extend stories with real Monday news).
2. `python3 render.py` — rebuilds `entry.png` (needs Pillow, Noto
   fonts, and `/tmp/ne_110m_land.geojson` — Natural Earth 110m land,
   sha256 `9e0729ee253ca7d7a5c4ae9395fb1902264c5377c52e224d13dd85010e2835d9`).
3. `python3 embed.py` — regenerates `main.ts` from the new PNG.
4. `rm -rf /output && node main.ts && sha256sum /output/entry.png`
   twice — both runs must print the same hash; check the PNG is
   1024×1024 and ≤ 1 MiB, and view it once.

## Verify (as shipped)

```
rm -rf /output && node main.ts && sha256sum /output/entry.png
# run again -> identical sha256: 53ebc7cedd739ea16a9e5083bd82bbc48d962ebe2d1647a303a5482a28cffa4f
```

## Refresh — Monday 23 November 2026 (this session, subagent 7a7d3e8a)

The Sunday build was refreshed with genuine Monday news before submitting.
See `sources.json` for the per-story source list (outlet + links) and the
corrections log, and `HANDOFF.md` (appended section) for the full refresh log.

- Heroes now: COP31 collapses (no deal) · Dymer toll corrected 14 missing → **11 dead** · **NEW: Ukraine sinks the Russian corvette Merkury off Libya** (7 sea drones, Benghazi).
- New mediums: AI sell-off (Nikkei −5.06% was **Friday 20 Nov**, not Monday — dated correctly), Democrats take the House (258 seats, largest since 1992). Alcaraz replaces the unverified Wembanyama item; Indonesia ship seizure replaces the single-source bomber item; the MQ-9 item is labelled CLAIM.
- Photos: 3 heroes + Sparta II are AI-generated photorealistic news-style images (`photos/`). Real wire photos were evaluated and rejected (wrong date/event, watermarked, or copyrighted) — see `sources.json` → `rejected_real_photos`. Remaining cards use original drawings made in code.
- Verification (2026-11-23 ~20:00 WITA): entry.png 1024×1024 RGB, **405,176 bytes**, sha256 `c42cc37c859fe177f1bd9a229455d7e648aa3b6fdfa509d3df33a95776dbd7e9`. `node main.ts` run twice → identical bytes (deterministic). Thumbnail test at 120 px: masthead + 3 photo heroes + map read clearly.
- Repo: anchor `67c26321316fa099e1aa09b545c2af42da95309f` (drand round 34210586, ≥ required 34196212), MIT LICENSE, entry commit `9b5c308` (full sha in HANDOFF.md).
- NOT submitted yet. Remaining before submit (parent runs these after this subagent finishes, so usage rows exist): bundle transcripts with `--provider meta --effort default --mcp none --prompt-file <Rifky's verbatim words> --prompt-origin handed-off --prompt-via "<one line>" --muse-usage <from muse.db>`, then check, then submit (see HANDOFF.md for exact commands).
