"""Auto-farm loop — walks the coin/map rotation and emits inject payloads."""
from __future__ import annotations

import time

from mm2_host.contracts.plugin import PluginContext

FARM_SCRIPT = """
-- mm2 auto_farm v1.2
local Players = game:GetService("Players")
local lp = Players.LocalPlayer
while true do
  task.wait(1.5)
  for _, coin in ipairs(workspace:GetChildren()) do
    if coin.Name == "Coin" then
      lp.Character.HumanoidRootPart.CFrame = coin.CFrame
    end
  end
end
"""


class AutoFarm:
    slug = "auto_farm"
    version = "1.2.0"
    provides = ("auto_farm",)

    def __init__(self) -> None:
        self.running = False
        self.started_at = 0.0

    def on_load(self, ctx: PluginContext) -> None:
        self.ctx = ctx

    def on_unload(self) -> None:
        self.running = False

    def handle(self, event: str, payload: dict) -> dict:
        if event == "start":
            self.running = True
            self.started_at = time.time()
            return {"inject": FARM_SCRIPT}
        if event == "stop":
            self.running = False
            return {"stopped": True, "ran_for": time.time() - self.started_at}
        return {"running": self.running}


PLUGIN = AutoFarm