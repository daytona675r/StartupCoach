import streamlit as st
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
import os
import json
from urllib.parse import urlparse
from langgraph.graph import MessagesState, StateGraph
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import HumanMessage, AIMessage

# ---- CONFIG ----
PERSIST_DIR = "vector_db"
K = 3  # number of top results to retrieve

# ---- STATE MANAGEMENT ----
class ChatState(TypedDict):
    messages: Annotated[Sequence[HumanMessage | AIMessage], MessagesState]

# ---- CHAT MANAGER ----
class ChatManager:
    def __init__(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
        self.messages = st.session_state.messages

    def get_messages(self):
        return self.messages

    def export_as_json(self):
        return json.dumps([
            {"role": "human" if isinstance(m, HumanMessage) else "ai", "content": m.content}
            for m in self.get_messages()
        ], indent=2)

    def clear(self):
        st.session_state.messages = []
        self.messages = st.session_state.messages

chat_manager = ChatManager()

# ---- INITIALIZATION ----
st.set_page_config(page_title="Startup Coach", layout="wide")
st.title("🚀 Startup Coach")

@st.cache_resource(show_spinner=False)
def load_retriever():
    embedding = OpenAIEmbeddings()
    vectorstore = Chroma(persist_directory=PERSIST_DIR, embedding_function=embedding)
    return vectorstore.as_retriever(search_kwargs={"k": K})

@st.cache_resource(show_spinner=False)
def create_workflow():
    retriever = load_retriever()
    llm = ChatOpenAI(temperature=0.2)
    
    def retrieve_documents(state: ChatState):
        last_message = state["messages"][-1]
        docs = retriever.get_relevant_documents(last_message.content)
        return {"context": docs}
    
    def generate_response(state: ChatState, context):
        last_message = state["messages"][-1]
        context_str = "\n\n".join(doc.page_content for doc in context["context"])
        prompt = f"""Context: {context_str}
        
        Question: {last_message.content}
        
        Please provide a helpful response based on the context above."""
        
        response = llm.invoke(prompt)
        return {"messages": state["messages"] + [AIMessage(content=response.content)]}
    
    # Create the workflow
    workflow = StateGraph(ChatState)
    
    # Add nodes
    workflow.add_node("retrieve", retrieve_documents)
    workflow.add_node("generate", generate_response)
    
    # Add edges
    workflow.add_edge("retrieve", "generate")
    workflow.set_entry_point("retrieve")
    workflow.set_finish_point("generate")
    
    return workflow.compile()

# ---- MAIN APP ----
workflow = create_workflow()
query = st.text_input("Ask a startup question:", placeholder="e.g. How do I start a startup?", key="query_input")

if query:
    with st.chat_message("user"):
        st.markdown(query)
    
    # Add user message to state
    chat_manager.messages.append(HumanMessage(content=query))
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Run the workflow
            result = workflow.invoke({"messages": chat_manager.messages})
            
            # Update messages with the response
            chat_manager.messages = result["messages"]
            
            # Display the response
            response = result["messages"][-1].content
            st.write(response)

# ---- CHAT HISTORY DISPLAY ----
st.subheader("💬 Chat History")
chat_container = st.container()
with chat_container:
    for msg in chat_manager.get_messages():
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.markdown(msg.content)
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(msg.content)

st.sidebar.subheader("📤 Export Chat")
chat_json = chat_manager.export_as_json()
st.sidebar.download_button(
    label="💾 Download Chat as JSON",
    data=chat_json,
    file_name="chat_history.json",
    mime="application/json"
)

# ---- CLEAR BUTTON ----
if st.sidebar.button("🧹 Clear Chat History"):
    chat_manager.clear()
    st.sidebar.success("Chat history cleared.")
