"""Pydantic models for script manifests and payloads."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ScriptEntry(BaseModel):
    name: str
    capability: Literal["esp", "aimbot", "auto_farm", "skin_inject", "coin_dropper"]
    enabled: bool = True
    priority: int = Field(default=5, ge=1, le=10)


class ExtensionManifest(BaseModel):
    slug: str
    version: str
    provides: list[str]
    scripts: list[ScriptEntry] = Field(default_factory=list)
    author: str = "mm2-community"