from demo_mode import DEMO_CANVAS, DEMO_CHAT, DEMO_NOTICE, DEMO_PITCH


def test_demo_is_deterministic_and_explicit():
    assert "No live model" in DEMO_NOTICE
    assert DEMO_CHAT["answer"]
    assert set(DEMO_CANVAS) == {"Problem", "Solution", "Target group"}
    assert len(DEMO_PITCH) == 3
