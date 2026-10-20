from calculators import calculate_runway
from translations import get_text


def test_runway_calculation_is_deterministic():
    assert calculate_runway(12000, 3000) == 4.0
    assert calculate_runway(12000, 0) == 0.0


def test_language_configuration():
    assert get_text("chat_input", "de")
    assert get_text("chat_input", "en")
