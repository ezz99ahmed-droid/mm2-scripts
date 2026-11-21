"""ESP overlay extension — draws player boxes/name tags during active rounds."""
from __future__ import annotations

from mm2_core.round_state import RoundState
from mm2_host.contracts.plugin import PluginContext


class EspOverlayPlugin:
    slug = "esp_overlay"
    version = "1.4.2"
    provides = ("overlay", "esp")

    def __init__(self) -> None:
        self.state = RoundState()
        self.ctx: PluginContext | None = None

    def on_load(self, ctx: PluginContext) -> None:
        self.ctx = ctx
        ctx.log.info("esp_overlay ready")

    def on_unload(self) -> None:
        self.ctx = None

    def handle(self, event: str, payload: dict) -> dict:
        if event == "round.phase":
            self.state.transition(payload["phase"])
            return {"armed": self.state.scripts_armed}
        if event == "draw":
            if not self.state.scripts_armed:
                return {"boxes": []}
            return {"boxes": payload.get("players", [])}
        return {"ok": True}


PLUGIN = EspOverlayPlugin