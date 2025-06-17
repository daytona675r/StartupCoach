import streamlit as st

def display_getting_started():
    """Display the Getting Started section."""
    st.markdown("""
    - **Welcome to Startup Mentor!** This AI-powered platform helps you navigate your startup journey.
    - Use the chat interface to ask questions about startups, business, or entrepreneurship.
    - Explore the Tools tab for practical startup resources.
    - Your chat history can be exported for future reference.
    """)

def display_key_features():
    """Display the Key Features section."""
    st.markdown("""
    - **AI Chat Assistant**: Get instant answers to your startup questions
    - **Business Model Canvas**: Visualize your business model
    - **Burn Rate Calculator**: Calculate your startup's financial runway
    - **Pitch Deck Generator**: Create professional pitch decks
    - **Knowledge Base**: Access curated startup resources
    """)

def display_tools_guide():
    """Display the Tools Guide section."""
    st.markdown("""
    - **Business Model Canvas**: Fill in the 9 key components of your business model
    - **Burn Rate Calculator**: Input your monthly expenses and cash to calculate runway
    - **Pitch Deck Generator**: Create a compelling pitch deck with our templates
    """)

def display_best_practices():
    """Display the Best Practices section."""
    st.markdown("""
    - Be specific in your questions for better answers
    - Use the tools regularly to track your progress
    - Export your chat history for important discussions
    - Combine AI insights with professional advice
    """)

def display_faq():
    """Display the FAQ section."""
    st.markdown("""
    **Q: How accurate is the AI advice?**  
    A: The AI provides guidance based on startup best practices, but always validate with experts.
    
    **Q: Can I save my work?**  
    A: Yes, use the Export Chat History button to save your conversations.
    
    **Q: Is my data secure?**  
    A: Yes, we don't store your sensitive business information.
    """)

def display_rag_visualization():
    """Display the RAG process visualization in the sidebar."""
    st.markdown("### The RAG Process")
    
    # Add custom CSS for bullet points
    st.markdown("""
    <style>
    .small-text {
        font-size: 0.85em;
        color: #666666;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add interactive example selector
    example_type = st.radio(
        "Choose an example to follow:",
        ["Business Model", "Market Analysis", "Financial Planning"],
        horizontal=True
    )
    
    # Step 1
    col1, arrow1, col2 = st.columns([3, 1, 3])
    with col1:
        st.info("**1. Your Question**\n\nYou ask a question about startups")
        if example_type == "Business Model":
            st.markdown('<div class="small-text">**Example:** How do I create a business model canvas for my SaaS startup?</div>', unsafe_allow_html=True)
        elif example_type == "Market Analysis":
            st.markdown('<div class="small-text">**Example:** What\'s the market size for AI-powered productivity tools?</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="small-text">**Example:** How do I calculate my startup\'s burn rate?</div>', unsafe_allow_html=True)
    with arrow1:
        st.markdown("### →")
    with col2:
        st.info("**2. Knowledge Search**\n\nSystem searches startup knowledge base")
        st.markdown("""
        <div class="small-text">
        - Searches through curated startup resources
        - Identifies relevant documents and articles
        - Ranks information by relevance
        </div>
        """, unsafe_allow_html=True)
    
    # Step 2
    col3, arrow2, col4 = st.columns([3, 1, 3])
    with col3:
        st.info("**3. Context Retrieval**\n\nRelevant information is gathered")
        st.markdown("""
        <div class="small-text">
        - Extracts key insights from documents
        - Identifies patterns and best practices
        - Gathers supporting data and statistics
        </div>
        """, unsafe_allow_html=True)
    with arrow2:
        st.markdown("### →")
    with col4:
        st.info("**4. AI Processing**\n\nAI combines context with knowledge")
        st.markdown("""
        <div class="small-text">
        - Analyzes gathered information
        - Combines multiple sources
        - Prepares comprehensive response
        </div>
        """, unsafe_allow_html=True)
    
    # Step 3
    col5, arrow3, col6 = st.columns([3, 1, 3])
    with col5:
        st.info("**5. Response Generation**\n\nAI creates detailed answer")
        if example_type == "Business Model":
            st.markdown('<div class="small-text">**Example Response:** Here\'s how to structure your business model canvas...</div>', unsafe_allow_html=True)
        elif example_type == "Market Analysis":
            st.markdown('<div class="small-text">**Example Response:** The AI productivity tools market is valued at...</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="small-text">**Example Response:** To calculate your burn rate, follow these steps...</div>', unsafe_allow_html=True)
    with arrow3:
        st.markdown("### →")
    with col6:
        st.info("**6. Source Display**\n\nSources are shown for verification")
        st.markdown("""
        <div class="small-text">
        - Links to original sources
        - Citations and references
        - Additional reading materials
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Interactive benefits section
    st.markdown("### 💡 How it helps you:")
    benefits = {
        "Get accurate, up-to-date startup information": "Access the latest startup trends and best practices",
        "Access verified sources and references": "All information comes from trusted startup resources",
        "Receive comprehensive, context-aware answers": "Get detailed responses tailored to your specific situation",
        "Make informed decisions with confidence": "Base your decisions on verified information and expert insights"
    }
    
    for benefit, tooltip in benefits.items():
        st.markdown(f"- {benefit}", help=tooltip)
    
    # Add a feedback section
    st.markdown("---")
    st.markdown("### Was this helpful?")
    feedback = st.radio(
        "Select your feedback:",
        ["👍 Very helpful", "👌 Somewhat helpful", "👎 Not helpful"],
        horizontal=True,
        label_visibility="collapsed"
    ) 