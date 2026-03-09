import streamlit as st
import os, sys
import plotly.graph_objects as go

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.calculators import calculate_emi, calculate_sip, calculate_fd

st.set_page_config(page_title="Financial Calculators", page_icon="🧮", layout="wide")

# Read CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🧮 Financial Calculators")
st.markdown("Plan your investments and loans efficiently.")

# Create tabs for different calculators
tab1, tab2, tab3 = st.tabs(["🏡 EMI Calculator", "📈 SIP Growth Calculator", "🏦 FD Return Calculator"])

# -----------------
# Tab 1: EMI Calculator
# -----------------
with tab1:
    st.header("Equated Monthly Installment (EMI)")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        principal_emi = st.number_input("Loan Amount ($)", min_value=0, value=50000, step=1000, key="emi_p")
        rate_emi = st.number_input("Annual Interest Rate (%)", min_value=0.0, value=8.5, step=0.1, key="emi_r")
        tenure_years_emi = st.number_input("Loan Tenure (Years)", min_value=1, value=5, step=1, key="emi_t")
        tenure_months_emi = tenure_years_emi * 12
    
    # Calculate
    emi, tot_interest_emi, tot_payment_emi = calculate_emi(principal_emi, rate_emi, tenure_months_emi)
    
    with col2:
        st.write("### Review:")
        st.metric("Your Monthly EMI", f"${emi:,.2f}")
        st.metric("Total Interest Payable", f"${tot_interest_emi:,.2f}")
        st.metric("Total Payment (Principal + Interest)", f"${tot_payment_emi:,.2f}")
        
    # Chart
    labels = ['Principal Loan Amount', 'Total Interest']
    values = [principal_emi, tot_interest_emi]
    fig_emi = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker_colors=['#4facfe', '#ff3366'])])
    fig_emi.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#f0f2f6'))
    st.plotly_chart(fig_emi, use_container_width=True)

# -----------------
# Tab 2: SIP Calculator
# -----------------
with tab2:
    st.header("Systematic Investment Plan (SIP)")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        monthly_inv_sip = st.number_input("Monthly Investment amount ($)", min_value=0, value=500, step=100, key="sip_p")
        expected_rate_sip = st.number_input("Expected Annual Return (%)", min_value=0.0, value=12.0, step=0.5, key="sip_r")
        tenure_sip = st.number_input("Time Period (Years)", min_value=1, value=10, step=1, key="sip_t")
        
    # Calculate
    total_invested_sip, returns_sip, total_value_sip = calculate_sip(monthly_inv_sip, expected_rate_sip, tenure_sip)
    
    with col2:
        st.write("### Review:")
        st.metric("Total Invested Amount", f"${total_invested_sip:,.2f}")
        st.metric("Est. Wealth Gained", f"${returns_sip:,.2f}")
        st.metric("Total Expected Returns", f"${total_value_sip:,.2f}")
        
    # Chart
    labels = ['Invested Amount', 'Wealth Gained']
    values = [total_invested_sip, returns_sip]
    fig_sip = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker_colors=['#00ff87', '#4facfe'])])
    fig_sip.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#f0f2f6'))
    st.plotly_chart(fig_sip, use_container_width=True)

# -----------------
# Tab 3: FD Calculator
# -----------------
with tab3:
    st.header("Fixed Deposit Return")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        principal_fd = st.number_input("Total Investment ($)", min_value=0, value=10000, step=1000, key="fd_p")
        rate_fd = st.number_input("Rate of Interest (%)", min_value=0.0, value=6.5, step=0.1, key="fd_r")
        tenure_fd = st.number_input("Time Period (Years)", min_value=1, value=5, step=1, key="fd_t")
        compounding = st.selectbox("Compounding Frequency", ["Quarterly (4)", "Half-Yearly (2)", "Yearly (1)"], index=0)
        
        freq_map = {"Quarterly (4)": 4, "Half-Yearly (2)": 2, "Yearly (1)": 1}
        freq_val = freq_map[compounding]
        
    val_p_fd, val_i_fd, val_mat_fd = calculate_fd(principal_fd, rate_fd, tenure_fd, freq_val)
    
    with col2:
        st.write("### Review:")
        st.metric("Invested Amount", f"${val_p_fd:,.2f}")
        st.metric("Total Interest Earned", f"${val_i_fd:,.2f}")
        st.metric("Total Maturity Value", f"${val_mat_fd:,.2f}")
        
    # Chart
    labels = ['Invested Amount', 'Interest Earned']
    values = [val_p_fd, val_i_fd]
    fig_fd = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker_colors=['#4facfe', '#af4261'])])
    fig_fd.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#f0f2f6'))
    st.plotly_chart(fig_fd, use_container_width=True)
