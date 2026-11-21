"""Tracks the current round phase so scripts know when to fire aimbot/esp handlers."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Phase(str, Enum):
    LOBBY = "lobby"
    ROLE_REVEAL = "role_reveal"
    ACTIVE = "active"
    POST_ROUND = "post_round"


@dataclass(slots=True)
class RoundState:
    phase: Phase = Phase.LOBBY
    round_no: int = 0
    innocent_alive: int = 0
    murderer_alive: int = 0
    sheriff_alive: int = 0

    def transition(self, new_phase: Phase) -> bool:
        allowed = {
            Phase.LOBBY: {Phase.ROLE_REVEAL},
            Phase.ROLE_REVEAL: {Phase.ACTIVE},
            Phase.ACTIVE: {Phase.POST_ROUND},
            Phase.POST_ROUND: {Phase.LOBBY},
        }
        if new_phase not in allowed[self.phase]:
            return False
        self.phase = new_phase
        if new_phase is Phase.ROLE_REVEAL:
            self.round_no += 1
        return True

    @property
    def scripts_armed(self) -> bool:
        return self.phase in (Phase.ROLE_REVEAL, Phase.ACTIVE)