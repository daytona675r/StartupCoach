from calculators import generate_business_model_canvas, generate_pitch_deck
from translations import get_text


def test_business_model_canvas_has_core_sections():
    canvas = generate_business_model_canvas("a note-taking tool for founders")
    assert "Problem" in canvas
    assert "Solution" in canvas


def test_pitch_deck_is_deterministic():
    first = generate_pitch_deck("a note-taking tool for founders")
    second = generate_pitch_deck("a note-taking tool for founders")
    assert first == second
    assert first


def test_language_configuration():
    assert get_text("chat_input", "de")
    assert get_text("chat_input", "en")
