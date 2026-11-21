from mm2_core.skin_engine import build_skin_payload, resolve_skin


def test_resolve_chroma():
    r = resolve_skin("Chroma Laser")
    assert r.tier == "chroma"
    assert r.asset_id == 3310


def test_build_payload_unknown():
    try:
        build_skin_payload(["not_a_skin"])
    except KeyError:
        return
    raise AssertionError("expected KeyError")