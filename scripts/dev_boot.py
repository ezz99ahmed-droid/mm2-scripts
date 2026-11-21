"""Dev helper: boots the host against a fake executor and runs one dispatch tick."""
from __future__ import annotations

from pathlib import Path

from mm2_host.bootstrap import HostBootstrap


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    host = HostBootstrap(root)
    reg = host.boot()

    reg.dispatch("esp", "round.phase", {"phase": "role_reveal"})
    out = reg.dispatch("aimbot", "tick", {"view": (0.0, 0.0), "players": [
        {"name": "xX_sheriff_Xx", "role": "sheriff", "x": 1.0, "y": 1.0},
        {"name": "murdererMain", "role": "murderer", "x": 5.0, "y": 3.0},
    ]})
    print("aimbot:", out)
    host.shutdown()


if __name__ == "__main__":
    main()