"""Skin/knife registry — resolves cosmetic names to in-game asset ids for script payloads."""
from __future__ import annotations

from dataclasses import dataclass

KNOWN_SKINS: dict[str, int] = {
    "chroma_laser": 3310,
    "chroma_darkbringer": 3311,
    "chroma_seer": 3312,
    "godly_gingerbread": 2201,
    "godly_icebreaker": 2210,
    "ancient_amerilaser": 4401,
}


@dataclass(slots=True)
class SkinResolution:
    name: str
    asset_id: int
    tier: str


def resolve_skin(name: str) -> SkinResolution:
    key = name.strip().lower().replace(" ", "_")
    if key not in KNOWN_SKINS:
        raise KeyError(f"unknown mm2 skin: {name!r}")
    asset_id = KNOWN_SKINS[key]
    tier = "chroma" if key.startswith("chroma") else "godly" if key.startswith("godly") else "ancient"
    return SkinResolution(name=key, asset_id=asset_id, tier=tier)


def build_skin_payload(names: list[str]) -> list[dict]:
    return [
        {"name": r.name, "assetId": r.asset_id, "tier": r.tier}
        for r in (resolve_skin(n) for n in names)
    ]