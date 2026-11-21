# Contributing to mm2-scripts

## Extensions
Drop a new folder under `extensions/<slug>/plugin.py` and export `PLUGIN`.
Keep `provides` capabilities small and unique.

## Style
- Python 3.12, `from __future__ import annotations` at top.
- No new deps without adding to `requirements.txt`.

## Tests
`pytest -q` must pass. Add a test per new service in `mm2_core/`.

## Legal
For educational/private-server use only. Don't submit anything that
bypasses anti-cheat on public Roblox servers — this repo is community
scripting research.