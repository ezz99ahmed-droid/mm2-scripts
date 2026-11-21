"""Aimbot core — lock target selection + smoothing tuned for MM2 throwables."""
from __future__ import annotations

import math

from mm2_host.contracts.plugin import PluginContext


class AimbotCore:
    slug = "aimbot_core"
    version = "2.0.1"
    provides = ("aimbot",)

    def __init__(self) -> None:
        self.smoothing = 0.35
        self.fov = 180.0
        self.locked_target: str | None = None

    def on_load(self, ctx: PluginContext) -> None:
        cfg = ctx.extras.get("aimbot", {})
        self.smoothing = float(cfg.get("smoothing", self.smoothing))
        self.fov = float(cfg.get("fov", self.fov))

    def on_unload(self) -> None:
        self.locked_target = None

    def _angle_delta(self, a: tuple[float, float], b: tuple[float, float]) -> float:
        dx, dy = b[0] - a[0], b[1] - a[1]
        return math.degrees(math.atan2(dy, dx))

    def handle(self, event: str, payload: dict) -> dict:
        if event != "tick":
            return {"ok": True}
        players = payload.get("players", [])
        murderer = next((p for p in players if p.get("role") == "murderer"), None)
        if murderer is None:
            self.locked_target = None
            return {"aim": None}
        delta = self._angle_delta(payload["view"], (murderer["x"], murderer["y"]))
        if abs(delta) > self.fov / 2:
            return {"aim": None}
        self.locked_target = murderer["name"]
        return {"aim": delta * self.smoothing, "target": self.locked_target}


PLUGIN = AimbotCore