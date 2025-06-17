from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langgraph.graph import StateGraph
from typing import TypedDict, Dict, Any, List
from langchain_core.messages import AIMessage, BaseMessage
import streamlit as st

@st.cache_resource(show_spinner=False)
def load_retriever():
    embedding = OpenAIEmbeddings()
    vectorstore = Chroma(persist_directory="vector_db", embedding_function=embedding)
    return vectorstore.as_retriever(search_kwargs={"k": 3})

@st.cache_resource(show_spinner=False)
def create_workflow():
    retriever = load_retriever()
    llm = ChatOpenAI(temperature=0.2)
    
    def is_startup_related(question: str) -> bool:
        """Check if the question is related to startups, business, or entrepreneurship."""
        prompt = f"""Given the following question, determine if it's related to startups, business, entrepreneurship, or general business advice.
        Answer with only 'yes' or 'no'.
        
        Question: {question}
        
        Is this question related to startups, business, or entrepreneurship?"""
        
        response = llm.invoke(prompt)
        return response.content.strip().lower() == 'yes'
    
    def retrieve_documents(state: Dict[str, Any]) -> Dict[str, Any]:
        messages = state["messages"]
        last_message = messages[-1]
        
        # Check if the question is startup-related
        if not is_startup_related(last_message.content):
            return {
                "messages": messages,
                "context": [],
                "is_startup_related": False
            }
        
        docs = retriever.get_relevant_documents(last_message.content)
        return {
            "messages": messages,
            "context": docs,
            "is_startup_related": True
        }
    
    def generate_response(state: Dict[str, Any]) -> Dict[str, Any]:
        messages = state["messages"]
        context = state.get("context", [])
        is_startup_related = state.get("is_startup_related", True)
        last_message = messages[-1]
        
        if not is_startup_related:
            # For non-startup questions, use the LLM directly
            prompt = f"""You are a helpful AI assistant. Please answer the following question:
            
            {last_message.content}"""
            
            response = llm.invoke(prompt)
            return {
                "messages": messages + [AIMessage(content=response.content)],
                "context": [],
                "is_startup_related": False
            }
        
        # For startup-related questions, use context
        context_str = "\n\n".join(doc.page_content for doc in context)
        prompt = f"""Context: {context_str}
        
        Question: {last_message.content}
        
        Please provide a helpful response based on the context above."""
        
        response = llm.invoke(prompt)
        return {
            "messages": messages + [AIMessage(content=response.content)],
            "context": context,
            "is_startup_related": True
        }
    
    class WorkflowState(TypedDict):
        messages: List[BaseMessage]
        context: List[Any]
        is_startup_related: bool
    
    workflow = StateGraph(WorkflowState)
    workflow.add_node("retrieve", retrieve_documents)
    workflow.add_node("generate", generate_response)
    workflow.add_edge("retrieve", "generate")
    workflow.set_entry_point("retrieve")
    workflow.set_finish_point("generate")
    
    return workflow.compile() 