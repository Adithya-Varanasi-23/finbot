import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd

# Basic Dashboard configuration
st.set_page_config(page_title="Dashboard | FinAI", page_icon="📈", layout="wide")

# Read CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📈 Financial Health Dashboard")
st.markdown("Get a birds-eye view of your estimated financial standing based on modern budgeting rules (50/30/20).")

# Quick inputs for estimation
st.sidebar.header("Update Your Profile")
monthly_income = st.sidebar.number_input("Est. Monthly Income ($)", min_value=0, value=5000, step=500)
monthly_expenses = st.sidebar.number_input("Est. Monthly Expenses ($)", min_value=0, value=3000, step=100)
savings = monthly_income - monthly_expenses

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

safe_savings = max(0, savings)
health_score = int(min(100, max(0, (safe_savings / monthly_income) * 100 * 2.5))) if monthly_income > 0 else 0

with col1:
    st.metric("Monthly Income", f"${monthly_income:,.0f}")
with col2:
    st.metric("Monthly Expenses", f"${monthly_expenses:,.0f}")
with col3:
    st.metric("Est. Savings", f"${safe_savings:,.0f}")
with col4:
    # A simple pseudo-score calculation
    color = "normal" if health_score > 60 else "inverse"
    st.metric("Financial Health Score", f"{health_score}/100", delta_color=color)

st.markdown("---")

# Charts
st.subheader("Budget Breakdown (Actual vs 50/30/20 Rule)")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # Actual Breakdown
    actual_labels = ['Expenses', 'Savings']
    actual_values = [monthly_expenses, safe_savings]
    colors = ['#ff3366', '#00ff87']
    
    fig1 = go.Figure(data=[go.Pie(labels=actual_labels, values=actual_values, hole=.5, marker_colors=colors)])
    fig1.update_layout(
        title_text="Your Actual Split",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f0f2f6')
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    # Recommended Breakdown (50/30/20 Goal)
    rec_labels = ['Needs (50%)', 'Wants (30%)', 'Savings (20%)']
    rec_values = [monthly_income * 0.50, monthly_income * 0.30, monthly_income * 0.20]
    rec_colors = ['#4facfe', '#af4261', '#00ff87']
    
    fig2 = go.Figure(data=[go.Pie(labels=rec_labels, values=rec_values, hole=.5, marker_colors=rec_colors)])
    fig2.update_layout(
        title_text="Recommended 50/30/20 Rule",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f0f2f6')
    )
    st.plotly_chart(fig2, use_container_width=True)

# Tip Generator based on inputs
st.subheader("💡 Quick AI-Style Tip")
if health_score >= 80:
    st.success("Excellent! You're saving a substantial portion of your income. Consider redirecting your surplus to index funds (SIPs) to beat inflation.")
elif health_score >= 50:
    st.info("You're on track, but there's room for improvement. Review your 'wants' category and see if you can trim 10% of discretionary spending.")
else:
    st.warning("Your expenses are consuming most of your income. Focus on debt reduction, cancelling unused subscriptions, and building an emergency fund of 3-6 months. Head over to the Chatbot to ask how to get started!")

