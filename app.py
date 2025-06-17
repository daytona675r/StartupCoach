import streamlit as st
from chat_manager import ChatManager
from workflow_manager import create_workflow
from tools_manager import (
    display_business_model_canvas,
    display_burn_rate_calculator,
    display_pitch_deck_generator,
    ToolsManager
)
from langchain_core.messages import HumanMessage
import os
from urllib.parse import urlparse
from help_guide import (
    display_rag_visualization,
    display_getting_started,
    display_key_features,
    display_tools_guide,
    display_best_practices,
    display_faq
)
from tool_llm import ToolLLM
from dashboard import display_dashboard
from token_tracker import TokenTracker
from translations import get_text

# Set page config (must be first Streamlit command)
st.set_page_config(
    page_title="Startup Mentor",
    page_icon="🚀",
    layout="wide"
)

# Add custom CSS for chat layout
st.markdown("""
    <style>
        .main > div {
            padding-bottom: 5rem;
        }
        .stChatInput {
            position: fixed;
            bottom: 0;
            background-color: white;
            padding: 1rem;
            z-index: 999;
            width: 800px;
            left: 50%;
            transform: translateX(-50%);
        }
        @media (max-width: 900px) {
            .stChatInput {
                width: 90%;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state.language = "en"

# Initialize chat manager
chat_manager = ChatManager()

# Initialize workflow
workflow = create_workflow()

# Initialize the tool-specific LLM
tool_llm = ToolLLM()

# Initialize the tools manager
tools_manager = ToolsManager()

# Initialize token tracker
token_tracker = TokenTracker()

def process_tool_request(user_input: str) -> str:
    """
    Process tool-specific requests using the dedicated GPT-3.5 model.
    """
    return tool_llm.process_tool_request(user_input)

def display_token_usage():
    """Display token usage in a subtle way."""
    usage = token_tracker.get_usage_summary()
    st.markdown(f"""
    <style>
    .token-usage {{
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: rgba(0, 0, 0, 0.6);
        padding: 8px 15px;
        border-radius: 8px;
        font-size: 0.9em;
        color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        z-index: 1000;
        font-family: monospace;
        line-height: 1.4;
    }}
    </style>
    <div class="token-usage">
        📊 Today: {usage['today_tokens']:,} tokens<br>
        💰 Cost: ${usage['today_cost']:.4f}<br>
        📈 Total: {usage['total_tokens']:,} tokens<br>
        💵 Total Cost: ${usage['total_cost']:.4f}
    </div>
    """, unsafe_allow_html=True)

def chat(user_input: str, chat_history: list) -> tuple:
    """
    Process the chat input and return the response.
    """
    # Check if the input is a tool request
    tool_keywords = ["generate", "calculate", "create", "build", "make"]
    is_tool_request = any(keyword in user_input.lower() for keyword in tool_keywords)
    
    if is_tool_request:
        # Use GPT-3.5 for tool-specific requests
        response = process_tool_request(user_input)
        # Track token usage for tool requests
        token_tracker.track_usage("gpt-3.5-turbo", user_input, response)
    else:
        # Use the main LLM for general conversation
        response = llm.invoke(user_input)
        # Track token usage for general conversation
        token_tracker.track_usage("gpt-4", user_input, response)
    
    # Update chat history
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": response})
    
    return response, chat_history

def display_language_selector():
    """Display language selector in the sidebar."""
    st.sidebar.selectbox(
        get_text("language_selector", st.session_state.language),
        ["English", "Deutsch"],
        index=0 if st.session_state.language == "en" else 1,
        key="language_selector",
        on_change=lambda: setattr(st.session_state, 'language', "de" if st.session_state.language_selector == "Deutsch" else "en")
    )

def display_chat_tab():
    """Display the chat interface."""
    st.markdown(get_text("chat_welcome", st.session_state.language))
    
    # Chat interface
    for message in chat_manager.get_messages():
        with st.chat_message("user" if isinstance(message, HumanMessage) else "assistant"):
            st.markdown(message.content)
    
    # Chat input
    if prompt := st.chat_input(get_text("chat_input", st.session_state.language)):
        # Add user message
        chat_manager.add_user_message(prompt)
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner(get_text("thinking", st.session_state.language)):
                # Run workflow
                result = workflow.invoke({
                    "messages": chat_manager.get_messages(),
                    "context": [],
                    "is_startup_related": True
                })
                
                # Get the response content
                response_content = result["messages"][-1].content
                
                # Track token usage
                token_tracker.track_usage("gpt-4", prompt, response_content)
                
                # Add AI response
                chat_manager.add_ai_message(response_content)
                
                # Display response
                st.markdown(response_content)
                
                # Display context for startup-related questions
                if result.get("is_startup_related", True) and "context" in result and result["context"]:
                    st.markdown("---")
                    st.markdown(f"**{get_text('sources', st.session_state.language)}**")
                    for i, doc in enumerate(result["context"], 1):
                        source = doc.metadata.get("source", "Unknown")
                        if source.endswith(".pdf"):
                            source_display = os.path.basename(source)
                        else:
                            parsed = urlparse(source)
                            source_display = parsed.netloc.replace("www.", "")
                        
                        # Display source and preview
                        preview = doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content
                        st.markdown(f"""
                            <div style='font-size: 0.8em; color: #666; margin: 5px 0;'>
                                <strong>Source {i}:</strong> {source_display}<br>
                                <em>{preview}</em>
                            </div>
                        """, unsafe_allow_html=True)
                elif result.get("is_startup_related", True):
                    st.markdown("---")
                    st.markdown(f"*{get_text('no_sources', st.session_state.language)}*")

def display_tools_tab():
    """Display the Tools tab content."""
    st.title(get_text("tools_title", st.session_state.language))
    
    # Business Model Canvas
    with st.expander(f"🎨 {get_text('bmc_title', st.session_state.language)}"):
        st.subheader(get_text("bmc_title", st.session_state.language))
        problem = st.text_area(get_text("problem", st.session_state.language))
        solution = st.text_area(get_text("solution", st.session_state.language))
        target_group = st.text_area(get_text("target_group", st.session_state.language))
        
        if st.button(get_text("generate_bmc", st.session_state.language)):
            input_data = f"""
            Problem Statement: {problem}
            Solution: {solution}
            Target Group: {target_group}
            """
            result = tools_manager.execute_tool("business_model_canvas", input_data)
            st.markdown(result)
    
    # Pitch Deck Generator
    with st.expander(f"🎯 {get_text('pitch_title', st.session_state.language)}"):
        st.subheader(get_text("pitch_title", st.session_state.language))
        problem = st.text_area(get_text("problem", st.session_state.language), key="pitch_problem")
        solution = st.text_area(get_text("solution", st.session_state.language), key="pitch_solution")
        target_group = st.text_area(get_text("target_group", st.session_state.language), key="pitch_target")
        
        if st.button(get_text("generate_pitch", st.session_state.language)):
            input_data = f"""
            Problem Statement: {problem}
            Solution: {solution}
            Target Group: {target_group}
            """
            result = tools_manager.execute_tool("pitch_deck", input_data)
            st.markdown(result)

# Sidebar
with st.sidebar:
    st.title("🚀 Startup Mentor")
    st.markdown("""
    Your AI-powered startup advisor. Get help with:
    - Business strategy
    - Market analysis
    - Financial planning
    - Pitch deck creation
    - And more!
    """)
    
    # Help Guide Section
    st.markdown("---")
    st.subheader("📚 Help Guide")
    
    # Getting Started Section
    with st.expander("🚀 Getting Started"):
        display_getting_started()
    
    # RAG Process Visualization
    with st.expander("🔄 How It Works"):
        display_rag_visualization()
    
    # Features Section
    with st.expander("✨ Key Features"):
        display_key_features()
    
    # Tools Guide Section
    with st.expander("🛠️ Tools Guide"):
        display_tools_guide()
    
    # Best Practices Section
    with st.expander("💡 Best Practices"):
        display_best_practices()
    
    # FAQ Section
    with st.expander("❓ FAQ"):
        display_faq()
    
    st.markdown("---")
    
    # Export chat history
    if st.button("Export Chat History"):
        chat_json = chat_manager.export_messages()
        st.download_button(
            label="Download Chat History",
            data=chat_json,
            file_name="chat_history.json",
            mime="application/json"
        )
    
    # Clear chat
    if st.button("Clear Chat"):
        chat_manager.clear_messages()
        st.rerun()

# Main app
st.title(get_text("app_title", st.session_state.language))

# Create tabs
tab1, tab2, tab3 = st.tabs([
    get_text("chat_tab", st.session_state.language),
    get_text("tools_tab", st.session_state.language),
    get_text("dashboard_tab", st.session_state.language)
])

# Display language selector in sidebar
display_language_selector()

with tab1:
    display_chat_tab()

with tab2:
    display_tools_tab()

with tab3:
    display_dashboard()

# Display token usage
display_token_usage()
