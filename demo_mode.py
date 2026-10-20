"""Deterministic, credential-free Streamlit presentation for portfolio review."""

from __future__ import annotations

from typing import Final


DEMO_NOTICE: Final[str] = "Demo mode: replayed example output. No live model or paid API call is made."

DEMO_CHAT = {
    "question": "How should a small B2B startup validate its first target segment?",
    "answer": "Start with one narrowly defined segment, test the problem through structured interviews, and record evidence before expanding the offer.",
}

DEMO_CANVAS = {
    "Problem": "Early teams lack a repeatable way to test which customer problem is urgent.",
    "Solution": "A guided evidence journal for interviews, assumptions and decisions.",
    "Target group": "Small B2B founders validating an initial market.",
}

DEMO_PITCH = [
    "Problem: founders often collect opinions without a traceable validation loop.",
    "Approach: capture assumptions, evidence and decisions in one lightweight workflow.",
    "Next step: run five interviews in one segment and compare the recorded signals.",
]


def render_demo(st) -> None:
    st.set_page_config(page_title="StartupCoach · Demo", page_icon="🚀", layout="wide")
    st.title("🚀 StartupCoach")
    st.info(DEMO_NOTICE)
    st.caption("Representative sample data for portfolio review; it is not a live AI session.")

    chat, tools, analytics = st.tabs(["Mentor chat", "Startup tools", "Analytics"])
    with chat:
        st.markdown(f"**Example question**  \n{DEMO_CHAT['question']}")
        st.markdown(f"**Replayed mentor response**  \n{DEMO_CHAT['answer']}")
        st.caption("Source context: simulated startup-validation notes")
    with tools:
        st.subheader("Business Model Canvas · example")
        for key, value in DEMO_CANVAS.items():
            st.markdown(f"**{key}**  \n{value}")
        st.subheader("Pitch-deck outline · example")
        for line in DEMO_PITCH:
            st.markdown(f"- {line}")
    with analytics:
        st.metric("Example tokens", "1,284")
        st.metric("Example cost", "$0.00")
        st.bar_chart({"mentor chat": 1, "canvas": 1, "pitch deck": 1})
