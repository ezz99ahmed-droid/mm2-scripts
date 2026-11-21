from mm2_core.round_state import Phase, RoundState


def test_transitions():
    s = RoundState()
    assert not s.scripts_armed
    assert s.transition(Phase.ROLE_REVEAL)
    assert s.scripts_armed
    assert s.round_no == 1
    assert s.transition(Phase.ACTIVE)
    assert s.transition(Phase.POST_ROUND)
    assert not s.scripts_armed