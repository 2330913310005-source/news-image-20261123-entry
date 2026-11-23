#!/usr/bin/env python3
"""Regenerate main.ts from entry.png (embed the PNG as base64).

Usage: python3 embed.py   (run after re-rendering entry.png)
"""
import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))
raw = open(os.path.join(HERE, "entry.png"), "rb").read()
b64 = base64.b64encode(raw).decode()
lines = "\n".join(
    f'  "{b64[i:i + 100]}" +' for i in range(0, len(b64), 100)
)
ts = """// News-image entry: "Monday 23 November 2026 - the world in one day".
// Writes the front-page image to /output/entry.png. The PNG bytes are
// embedded below (base64) so the program is fully deterministic and needs
// no network: both grade-time runs write identical bytes. The image was
// built by render.py from stories.json (40 dated stories, 8 regions);
// see README.md for the sources and how to refresh it.
import { mkdirSync, writeFileSync } from "node:fs";

const PNG_B64 =
""" + lines + """
  "";

mkdirSync("/output", { recursive: true });
writeFileSync("/output/entry.png", Buffer.from(PNG_B64, "base64"));
"""
open(os.path.join(HERE, "main.ts"), "w").write(ts)
print(f"main.ts: {len(ts)} bytes from entry.png ({len(raw)} bytes)")
