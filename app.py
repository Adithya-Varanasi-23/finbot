import streamlit as st
import os

# App Configuration
st.set_page_config(
    page_title="AI Personal Finance Assistant",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
load_css("assets/style.css")

# Sidebar and Main Layout
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135673.png", width=60)
    st.title("FinAI Assistant")
    st.markdown("Your personal AI-powered financial advisor.")
    
    st.markdown("---")
    
    st.markdown("### Navigation")
    st.info("👈 Please select a module from the menu above to get started.")
    
    st.markdown("---")
    st.markdown("### Security Note")
    st.caption("🔒 All financial data processed is done in-memory. We do not store your CSVs, PDFs, or Personal Identifiable Information.")
    st.warning("⚠️ Disclamer: The AI advice provided in this app is for informational purposes only. Consult a certified financial planner for professional decisions.")

# Initialization check
api_key_found = False
if 'GEMINI_API_KEY' in os.environ:
    api_key_found = True
else:
    try:
        if 'GEMINI_API_KEY' in st.secrets:
            api_key_found = True
    except FileNotFoundError:
        pass
    except Exception:
        pass

if not api_key_found:
    st.sidebar.error("⚠️ GEMINI_API_KEY not found. Please configure it in .env or secrets to use AI features.")

# Main window Intro
st.title("💸 Welcome to FinAI")
st.markdown("""
<div style='padding: 20px; background-color: var(--panel); border-radius: 10px; margin-bottom: 20px; border: 1px solid var(--border)'>
    <h3 style='margin-top: 0px;'>Your Smart Journey to Financial Freedom Starts Here.</h3>
    <p style='color: var(--text-muted); font-size: 1.1rem;'>
        Leverage the power of Google's Gemini Advanced AI to take control of your savings, investments, and daily expenses. 
        Analyze bank statements, parse complex tax documents, and get real-time budgeting advice.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### 🤖 AI Chatbot
    Ask anything about budgeting, taxes, equity investments, or debt management.
    """)
with col2:
    st.markdown("""
    #### 🧮 Smart Calculators
    Plan your future with EMI, Systematic Investment Plan (SIP), and Fixed Deposit tools.
    """)
with col3:
    st.markdown("""
    #### 📊 Expense Analyst
    Upload your bank CSV statements to auto-categorize expenses and get a spending breakdown.
    """)
