TRANSLATIONS = {
    "en": {
        "app_title": "Startup Mentor",
        "chat_tab": "💬 Chat",
        "tools_tab": "🛠️ Tools",
        "dashboard_tab": "📊 Dashboard",
        "chat_welcome": "Ask me anything about startups, business, or entrepreneurship!",
        "chat_input": "What would you like to know?",
        "thinking": "Thinking...",
        "sources": "Sources:",
        "no_sources": "No sources available",
        "tools_title": "Startup Tools",
        "bmc_title": "Business Model Canvas Generator",
        "pitch_title": "Pitch Deck Generator",
        "problem": "Problem Statement",
        "solution": "Solution",
        "target_group": "Target Group",
        "generate_bmc": "Generate Business Model Canvas",
        "generate_pitch": "Generate Pitch Deck Structure",
        "help_guide": "Help Guide",
        "getting_started": "Getting Started",
        "key_features": "Key Features",
        "tools_guide": "Tools Guide",
        "best_practices": "Best Practices",
        "faq": "FAQ",
        "how_it_works": "How It Works",
        "language_selector": "Select Language",
    },
    "de": {
        "app_title": "Startup Mentor",
        "chat_tab": "💬 Chat",
        "tools_tab": "🛠️ Tools",
        "dashboard_tab": "📊 Dashboard",
        "chat_welcome": "Fragen Sie mich alles über Startups, Business oder Unternehmertum!",
        "chat_input": "Was möchten Sie wissen?",
        "thinking": "Denke...",
        "sources": "Quellen:",
        "no_sources": "Keine Quellen verfügbar",
        "tools_title": "Startup Tools",
        "bmc_title": "Business Model Canvas Generator",
        "pitch_title": "Pitch Deck Generator",
        "problem": "Problemstellung",
        "solution": "Lösung",
        "target_group": "Zielgruppe",
        "generate_bmc": "Business Model Canvas generieren",
        "generate_pitch": "Pitch Deck Struktur generieren",
        "help_guide": "Hilfe",
        "getting_started": "Erste Schritte",
        "key_features": "Hauptfunktionen",
        "tools_guide": "Tools Anleitung",
        "best_practices": "Best Practices",
        "faq": "FAQ",
        "how_it_works": "Wie es funktioniert",
        "language_selector": "Sprache auswählen",
    },
}


def get_text(key: str, lang: str = "en") -> str:
    """
    Get translated text for a given key and language.

    Args:
        key (str): The translation key
        lang (str): The language code (default: "en")

    Returns:
        str: The translated text
    """
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
