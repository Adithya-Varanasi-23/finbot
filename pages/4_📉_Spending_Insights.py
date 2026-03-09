import streamlit as st
import os, sys
import plotly.express as px

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_processing import process_expense_csv, get_spending_summary
from utils.gemini_helper import analyze_financial_data

st.set_page_config(page_title="Expense Analyzer", page_icon="📊", layout="wide")

# Read CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📊 Expense Analyzer")
st.markdown("Upload your bank statement (CSV) to get AI-powered insights on your spending habits.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    with st.spinner("Processing your statement..."):
        df = process_expense_csv(uploaded_file)
        
        if df.empty:
            st.error("Error processing file. Please ensure it is a valid bank statement CSV with Date, Description, and Amount columns.")
        else:
            st.success("File processed successfully!")
            
            # Show Raw Data Preview
            with st.expander("View Uploaded Transactions"):
                st.dataframe(df)
            
            summary_df = get_spending_summary(df)
            total_spent = summary_df['Amount'].sum()
            
            # Key Metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Expenses", f"${total_spent:,.2f}")
            with col2:
                top_cat = summary_df.iloc[0]['Category'] if not summary_df.empty else "N/A"
                st.metric("Top Spending Category", top_cat)
                
            st.markdown("---")
            
            # Visualize Data
            st.subheader("Spending Breakdown")
            
            fig = px.pie(summary_df, values='Amount', names='Category', hole=0.4, 
                         color_discrete_sequence=px.colors.sequential.Plasma)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#f0f2f6'))
            st.plotly_chart(fig, use_container_width=True)
            
            # Display Summary Table
            st.dataframe(summary_df, use_container_width=True)
            
            # Generate AI Insights
            st.markdown("---")
            st.subheader("💡 AI Financial Insights")
            
            if st.button("Generate Insights with Gemini", type="primary"):
                with st.spinner("Analyzing your spending patterns..."):
                    # Format summary data for prompt
                    data_string = summary_df.to_string(index=False)
                    insights = analyze_financial_data(data_string)
                    
                    st.markdown("""
                    <div style='background-color: var(--panel); padding: 20px; border-radius: 10px; border: 1px solid var(--accent); margin-top: 10px;'>
                        {}
                    </div>
                    """.format(insights.replace('\n', '<br>')), unsafe_allow_html=True)
