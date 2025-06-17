import streamlit as st
import json
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from typing import Sequence

class ChatState:
    messages: Sequence[BaseMessage]

class ChatManager:
    def __init__(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
        self.messages = st.session_state.messages

    def get_messages(self):
        return self.messages

    def add_user_message(self, content: str):
        """Add a user message to the chat."""
        self.messages.append(HumanMessage(content=content))
        st.session_state.messages = self.messages

    def add_ai_message(self, content: str):
        """Add an AI message to the chat."""
        self.messages.append(AIMessage(content=content))
        st.session_state.messages = self.messages

    def export_messages(self):
        """Export messages as JSON."""
        return json.dumps([
            {"role": "human" if isinstance(m, HumanMessage) else "ai", "content": m.content}
            for m in self.get_messages()
        ], indent=2)

    def clear_messages(self):
        """Clear all messages."""
        st.session_state.messages = []
        self.messages = st.session_state.messages 