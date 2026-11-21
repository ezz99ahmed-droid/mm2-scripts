from pathlib import Path

from mm2_host.bootstrap import HostBootstrap


def test_host_boots_extensions():
    root = Path(__file__).resolve().parents[1]
    host = HostBootstrap(root)
    reg = host.boot()
    slugs = {p.slug for p in reg.all()}
    assert {"esp_overlay", "aimbot_core", "auto_farm", "skin_inject"} <= slugs
    host.shutdown()