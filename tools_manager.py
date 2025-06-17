from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
import streamlit as st
from typing import Dict, Any
from calculators import (
    calculate_burn_rate,
    calculate_runway,
    generate_business_model_canvas,
    generate_pitch_deck
)
from pdf_generator import create_pitch_deck_pdf

class ToolsManager:
    def __init__(self):
        """Initialize the Tools Manager with GPT-3.5 for tool execution."""
        self.tool_llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Define tool-specific prompts
        self.tool_prompts = {
            "business_model_canvas": """You are a business model canvas expert. Generate a detailed business model canvas based on the following information:
            {input}
            
            Format the output as a structured business model canvas with the following sections:
            1. Key Partners
            2. Key Activities
            3. Key Resources
            4. Value Propositions
            5. Customer Relationships
            6. Channels
            7. Customer Segments
            8. Cost Structure
            9. Revenue Streams""",
            
            "burn_rate": """You are a financial analysis expert. Calculate the burn rate and provide financial insights based on the following data:
            {input}
            
            Include in your analysis:
            1. Monthly burn rate
            2. Runway calculation
            3. Key financial metrics
            4. Recommendations for improvement""",
            
            "pitch_deck": """You are a pitch deck expert. Create a comprehensive pitch deck structure based on the following information:
            {input}
            
            Include the following sections:
            1. Problem Statement
            2. Solution
            3. Market Opportunity
            4. Business Model
            5. Go-to-Market Strategy
            6. Financial Projections
            7. Team
            8. Ask"""
        }
    
    def execute_tool(self, tool_name: str, input_data: str) -> str:
        """
        Execute a specific tool using GPT-3.5.
        
        Args:
            tool_name (str): Name of the tool to execute
            input_data (str): Input data for the tool
            
        Returns:
            str: Tool execution result
        """
        if tool_name not in self.tool_prompts:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        # Create the prompt template for the specific tool
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.tool_prompts[tool_name]),
            ("human", "{input}")
        ])
        
        # Create and execute the chain
        chain = (
            {"input": RunnablePassthrough()}
            | prompt
            | self.tool_llm
            | StrOutputParser()
        )
        
        try:
            result = chain.invoke(input_data)
            return result
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"
    
    def display_tool_interface(self, tool_name: str):
        """
        Display the interface for a specific tool.
        
        Args:
            tool_name (str): Name of the tool to display
        """
        st.subheader(f"{tool_name.replace('_', ' ').title()}")
        
        if tool_name == "business_model_canvas":
            self._display_business_model_canvas_interface()
        elif tool_name == "burn_rate":
            self._display_burn_rate_interface()
        elif tool_name == "pitch_deck":
            self._display_pitch_deck_interface()
    
    def _display_business_model_canvas_interface(self):
        """Display the Business Model Canvas interface."""
        company_name = st.text_input("Company Name")
        industry = st.text_input("Industry")
        target_market = st.text_area("Target Market")
        value_proposition = st.text_area("Value Proposition")
        
        if st.button("Generate Business Model Canvas"):
            input_data = f"""
            Company Name: {company_name}
            Industry: {industry}
            Target Market: {target_market}
            Value Proposition: {value_proposition}
            """
            result = self.execute_tool("business_model_canvas", input_data)
            st.markdown(result)
    
    def _display_burn_rate_interface(self):
        """Display the Burn Rate Calculator interface."""
        monthly_expenses = st.number_input("Monthly Expenses ($)", min_value=0)
        current_cash = st.number_input("Current Cash Balance ($)", min_value=0)
        monthly_revenue = st.number_input("Monthly Revenue ($)", min_value=0)
        
        if st.button("Calculate Burn Rate"):
            input_data = f"""
            Monthly Expenses: ${monthly_expenses}
            Current Cash Balance: ${current_cash}
            Monthly Revenue: ${monthly_revenue}
            """
            result = self.execute_tool("burn_rate", input_data)
            st.markdown(result)
    
    def _display_pitch_deck_interface(self):
        """Display the Pitch Deck Generator interface."""
        company_name = st.text_input("Company Name")
        problem = st.text_area("Problem Statement")
        solution = st.text_area("Solution")
        market_size = st.text_input("Market Size")
        business_model = st.text_area("Business Model")
        
        if st.button("Generate Pitch Deck Structure"):
            input_data = f"""
            Company Name: {company_name}
            Problem Statement: {problem}
            Solution: {solution}
            Market Size: {market_size}
            Business Model: {business_model}
            """
            result = self.execute_tool("pitch_deck", input_data)
            st.markdown(result)

def display_business_model_canvas():
    """Display the Business Model Canvas Generator section."""
    st.subheader("🎨 Business Model Canvas Generator")
    
    problem_bmc = st.text_area("Problem Statement", key="problem_bmc")
    solution_bmc = st.text_area("Solution", key="solution_bmc")
    target_group_bmc = st.text_area("Target Group", key="target_group_bmc")
    
    if st.button("Generate Business Model Canvas"):
        if not all([problem_bmc, solution_bmc, target_group_bmc]):
            st.warning("Please fill in all required fields.")
            return
            
        with st.spinner("Generating Business Model Canvas..."):
            bmc = generate_business_model_canvas(
                problem=problem_bmc,
                solution=solution_bmc,
                target_group=target_group_bmc
            )
            
            st.markdown("### 🎨 Business Model Canvas")
            st.markdown("#### Key Partners")
            for partner in bmc["key_partners"]:
                st.markdown(f"- {partner}")
                
            st.markdown("#### Key Activities")
            for activity in bmc["key_activities"]:
                st.markdown(f"- {activity}")
                
            st.markdown("#### Value Propositions")
            for value in bmc["value_proposition"]:
                st.markdown(f"- {value}")
                
            st.markdown("#### Customer Relationships")
            for relationship in bmc["customer_relationships"]:
                st.markdown(f"- {relationship}")
                
            st.markdown("#### Customer Segments")
            for segment in bmc["customer_segments"]:
                st.markdown(f"- {segment}")
                
            st.markdown("#### Key Resources")
            for resource in bmc["key_resources"]:
                st.markdown(f"- {resource}")
                
            st.markdown("#### Channels")
            for channel in bmc["channels"]:
                st.markdown(f"- {channel}")
                
            st.markdown("#### Cost Structure")
            for cost in bmc["cost_structure"]:
                st.markdown(f"- {cost}")
                
            st.markdown("#### Revenue Streams")
            for revenue in bmc["revenue_streams"]:
                st.markdown(f"- {revenue}")

def display_burn_rate_calculator():
    """Display the Burn Rate & Runway Calculator section."""
    st.subheader("💰 Burn Rate & Runway Calculator")
    
    monthly_expenses = st.number_input("Monthly Expenses ($)", min_value=0.0, value=10000.0)
    current_cash = st.number_input("Current Cash Balance ($)", min_value=0.0, value=100000.0)
    
    if st.button("Calculate"):
        result = calculate_burn_rate(current_cash, monthly_expenses)
        burn_rate = result["burn_rate"]
        runway = calculate_runway(current_cash, burn_rate)
        
        st.markdown("### Results")
        st.markdown(f"**Monthly Burn Rate:** ${burn_rate:,.2f}")
        st.markdown(f"**Runway:** {runway:.1f} months")
        
        # Display warning level with appropriate color
        warning_level = result["warning_level"]
        if warning_level == "critical":
            st.error("⚠️ Critical Warning: Less than 3 months of runway")
        elif warning_level == "warning":
            st.warning("⚠️ Warning: 3-6 months of runway")
        else:
            st.success("✅ Healthy: More than 6 months of runway")
        
        # Display recommendation
        st.markdown("### Recommendation")
        st.markdown(result["recommendation"])

def display_pitch_deck_generator():
    """Display the Pitch Deck Generator section."""
    st.subheader("🎯 Pitch Deck Generator")
    
    problem_pd = st.text_area("Problem Statement", key="problem_pd")
    solution_pd = st.text_area("Solution", key="solution_pd")
    target_group_pd = st.text_area("Target Group", key="target_group_pd")
    business_model = st.text_area("Business Model (Optional)", key="business_model")
    market_size = st.text_area("Market Size (Optional)", key="market_size")
    funding_needed = st.text_area("Funding Needed (Optional)", key="funding_needed")
    
    if st.button("Generate Pitch Deck"):
        if not all([problem_pd, solution_pd, target_group_pd]):
            st.warning("Please fill in all required fields.")
            return
            
        with st.spinner("Generating Pitch Deck..."):
            pitch_deck = generate_pitch_deck(
                problem=problem_pd,
                solution=solution_pd,
                target_group=target_group_pd,
                business_model=business_model if business_model else None,
                market_size=market_size if market_size else None,
                funding_needed=funding_needed if funding_needed else None
            )
            
            st.markdown("### 📊 Pitch Deck Outline")
            
            # Title Slide
            st.markdown(f"#### {pitch_deck['title_slide']['company_name']}")
            st.markdown(f"*{pitch_deck['title_slide']['tagline']}*")
            
            # Problem Slide
            st.markdown("#### Problem")
            st.markdown(pitch_deck["problem_slide"]["main_problem"])
            st.markdown("**Key Pain Points:**")
            for point in pitch_deck["problem_slide"]["key_pain_points"]:
                st.markdown(f"- {point}")
            st.markdown("**Current Solutions:**")
            for solution in pitch_deck["problem_slide"]["current_solutions"]:
                st.markdown(f"- {solution}")
                
            # Solution Slide
            st.markdown("#### Solution")
            st.markdown(pitch_deck["solution_slide"]["main_solution"])
            st.markdown("**Key Features:**")
            for feature in pitch_deck["solution_slide"]["key_features"]:
                st.markdown(f"- {feature}")
            st.markdown(f"**Unique Value:** {pitch_deck['solution_slide']['unique_value']}")
                
            # Market Slide
            st.markdown("#### Market")
            st.markdown(f"**Target Market:** {pitch_deck['market_slide']['target_market']}")
            st.markdown(f"**Market Size:** {pitch_deck['market_slide']['market_size']}")
            st.markdown(f"**Growth Potential:** {pitch_deck['market_slide']['growth_potential']}")
            st.markdown("**Market Trends:**")
            for trend in pitch_deck["market_slide"]["market_trends"]:
                st.markdown(f"- {trend}")
                
            # Business Model Slide
            st.markdown("#### Business Model")
            st.markdown(f"**Revenue Model:** {pitch_deck['business_model_slide']['revenue_model']}")
            st.markdown("**Key Metrics:**")
            for metric in pitch_deck["business_model_slide"]["key_metrics"]:
                st.markdown(f"- {metric}")
            st.markdown("**Cost Structure:**")
            for cost in pitch_deck["business_model_slide"]["cost_structure"]:
                st.markdown(f"- {cost}")
                
            # Go-to-Market Slide
            st.markdown("#### Go-to-Market Strategy")
            st.markdown(f"**Strategy:** {pitch_deck['go_to_market_slide']['strategy']}")
            st.markdown("**Channels:**")
            for channel in pitch_deck["go_to_market_slide"]["channels"]:
                st.markdown(f"- {channel}")
            st.markdown("**Timeline:**")
            for milestone in pitch_deck["go_to_market_slide"]["timeline"]:
                st.markdown(f"- {milestone}")
                
            # Team Slide
            st.markdown("#### Team")
            st.markdown("**Key Roles:**")
            for role in pitch_deck["team_slide"]["key_roles"]:
                st.markdown(f"- {role}")
            st.markdown("**Team Strengths:**")
            for strength in pitch_deck["team_slide"]["team_strengths"]:
                st.markdown(f"- {strength}")
            st.markdown("**Hiring Plan:**")
            for hire in pitch_deck["team_slide"]["hiring_plan"]:
                st.markdown(f"- {hire}")
                
            # Financials Slide
            st.markdown("#### Financials")
            st.markdown(f"**Funding Needed:** {pitch_deck['financials_slide']['funding_needed']}")
            st.markdown("**Use of Funds:**")
            for use in pitch_deck["financials_slide"]["use_of_funds"]:
                st.markdown(f"- {use}")
            st.markdown("**Financial Projections:**")
            for projection in pitch_deck["financials_slide"]["financial_projections"]:
                st.markdown(f"- {projection}")
                
            # Call to Action Slide
            st.markdown("#### Call to Action")
            st.markdown("**Next Steps:**")
            for step in pitch_deck["call_to_action"]["next_steps"]:
                st.markdown(f"- {step}")
            st.markdown(f"**Contact Info:** {pitch_deck['call_to_action']['contact_info']}")
            st.markdown(f"**Investment Terms:** {pitch_deck['call_to_action']['investment_terms']}")
            
            # Add PDF download button
            pdf_bytes = create_pitch_deck_pdf(pitch_deck)
            st.download_button(
                label="Download Pitch Deck as PDF",
                data=pdf_bytes,
                file_name=f"{pitch_deck['title_slide']['company_name'].replace(' ', '_')}_Pitch_Deck.pdf",
                mime="application/pdf"
            ) 