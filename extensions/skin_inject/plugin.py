"""Skin inject extension — pushes cosmetic payloads through the executor bridge."""
from __future__ import annotations

from mm2_core.skin_engine import build_skin_payload
from mm2_host.contracts.plugin import PluginContext


class SkinInject:
    slug = "skin_inject"
    version = "0.9.4"
    provides = ("skin_inject",)

    def on_load(self, ctx: PluginContext) -> None:
        self.ctx = ctx

    def on_unload(self) -> None:
        pass

    def handle(self, event: str, payload: dict) -> dict:
        if event != "apply":
            return {"ok": True}
        try:
            resolved = build_skin_payload(payload.get("skins", []))
        except KeyError as exc:
            return {"ok": False, "error": str(exc)}
        return {"ok": True, "payload": resolved}


PLUGIN = SkinInject