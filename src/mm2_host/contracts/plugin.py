"""Shared plugin contract every MM2 extension implements."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol


@dataclass(slots=True)
class PluginContext:
    host_version: str
    data_dir: Path
    log: Any
    extras: dict[str, Any] = field(default_factory=dict)


class MM2Plugin(Protocol):
    slug: str
    version: str
    provides: tuple[str, ...]

    def on_load(self, ctx: PluginContext) -> None: ...

    def on_unload(self) -> None: ...

    def handle(self, event: str, payload: dict[str, Any]) -> dict[str, Any]: ...