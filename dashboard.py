import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def calculate_runway(monthly_expenses, current_cash, monthly_revenue):
    """Calculate runway and other financial metrics."""
    net_monthly_burn = monthly_expenses - monthly_revenue
    if net_monthly_burn <= 0:
        return {
            'runway_months': float('inf'),
            'net_monthly_burn': net_monthly_burn,
            'monthly_burn_rate': 0
        }
    
    runway_months = current_cash / net_monthly_burn
    monthly_burn_rate = (net_monthly_burn / current_cash) * 100
    
    return {
        'runway_months': runway_months,
        'net_monthly_burn': net_monthly_burn,
        'monthly_burn_rate': monthly_burn_rate
    }

def generate_cash_projection(current_cash, monthly_expenses, monthly_revenue, months=12):
    """Generate cash projection over time."""
    dates = [(datetime.now() + timedelta(days=30*x)).strftime('%Y-%m-%d') for x in range(months+1)]
    cash_balance = [current_cash]
    
    for _ in range(months):
        current_cash = current_cash - (monthly_expenses - monthly_revenue)
        cash_balance.append(max(0, current_cash))
    
    return pd.DataFrame({
        'Date': dates,
        'Cash Balance': cash_balance
    })

def generate_expense_breakdown(monthly_expenses):
    """Generate a breakdown of expenses by category."""
    # Example expense categories and their typical percentages
    categories = {
        'Salaries': 0.6,
        'Infrastructure': 0.15,
        'Marketing': 0.1,
        'Operations': 0.1,
        'Other': 0.05
    }
    
    return pd.DataFrame({
        'Category': list(categories.keys()),
        'Amount': [monthly_expenses * pct for pct in categories.values()]
    })

def get_risk_zone(runway_months):
    """Determine the risk zone based on runway months."""
    if runway_months >= 6:
        return "Safe Zone", "green"
    elif runway_months >= 3:
        return "Caution Zone", "orange"
    else:
        return "Danger Zone", "red"

def display_risk_zone(runway_months):
    """Display the risk zone indicator."""
    risk_zone, color = get_risk_zone(runway_months)
    
    # Create a custom HTML/CSS for the risk zone indicator
    st.markdown(f"""
    <style>
    .risk-zone {{
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        text-align: center;
        font-weight: bold;
        color: white;
        background-color: {color};
    }}
    </style>
    <div class="risk-zone">
        {risk_zone} - {runway_months:.1f} months runway
    </div>
    """, unsafe_allow_html=True)

def display_burn_rate_dashboard():
    """Display the burn rate dashboard with visualizations."""
    st.header("📊 Burn Rate Dashboard")
    
    # Input section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Financial Inputs")
        monthly_expenses = st.number_input("Monthly Expenses ($)", min_value=0, value=50000)
        current_cash = st.number_input("Current Cash Balance ($)", min_value=0, value=200000)
        monthly_revenue = st.number_input("Monthly Revenue ($)", min_value=0, value=10000)
    
    # Calculate metrics
    metrics = calculate_runway(monthly_expenses, current_cash, monthly_revenue)
    
    # Display risk zone
    display_risk_zone(metrics['runway_months'])
    
    # Display key metrics
    with col2:
        st.subheader("Key Metrics")
        st.metric(
            label="Runway",
            value=f"{metrics['runway_months']:.1f} months",
            delta=f"{metrics['monthly_burn_rate']:.1f}% monthly burn rate"
        )
        st.metric(
            label="Net Monthly Burn",
            value=f"${metrics['net_monthly_burn']:,.2f}",
            delta="per month"
        )
    
    # Generate data for visualizations
    cash_projection = generate_cash_projection(current_cash, monthly_expenses, monthly_revenue)
    expense_breakdown = generate_expense_breakdown(monthly_expenses)
    
    # Visualizations
    st.subheader("Cash Projection")
    fig = px.line(cash_projection, x='Date', y='Cash Balance',
                  title='Cash Balance Over Time',
                  labels={'Cash Balance': 'Cash Balance ($)', 'Date': 'Date'})
    fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Zero Cash")
    st.plotly_chart(fig, use_container_width=True)
    
    # Expense breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(expense_breakdown, values='Amount', names='Category',
                     title='Monthly Expenses Breakdown')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Monthly runway bar chart
        months = list(range(1, 13))
        runway_data = pd.DataFrame({
            'Month': months,
            'Runway': [metrics['runway_months'] - i for i in months]
        })
        runway_data['Runway'] = runway_data['Runway'].clip(lower=0)
        
        fig = px.bar(runway_data, x='Month', y='Runway',
                     title='Estimated Runway by Month',
                     labels={'Runway': 'Remaining Months', 'Month': 'Month'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Expense growth trend
    st.subheader("Expense Growth Trend")
    months = list(range(1, 13))
    growth_rate = 0.05  # 5% monthly growth
    expenses = [monthly_expenses * (1 + growth_rate) ** i for i in range(12)]
    
    fig = px.line(x=months, y=expenses,
                  title='Projected Expense Growth',
                  labels={'x': 'Month', 'y': 'Expenses ($)'})
    st.plotly_chart(fig, use_container_width=True)

def display_dashboard():
    """Main function to display the dashboard."""
    display_burn_rate_dashboard() 