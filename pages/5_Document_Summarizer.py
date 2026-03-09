import streamlit as st
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.pdf_processing import extract_text_from_pdf
from utils.gemini_helper import summarize_financial_document

st.set_page_config(page_title="Document Summarizer", page_icon="📄", layout="wide")

# Read CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📄 Financial Document Summarizer")
st.markdown("Upload tax reports, investment portfolios, or loan agreements to get a quick AI summary.")

uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

if uploaded_file is not None:
    # Check if a new file is uploaded
    if "current_file" not in st.session_state or st.session_state.current_file != uploaded_file.name:
        st.session_state.current_file = uploaded_file.name
        st.session_state.extracted_text = None
        st.session_state.summary = None

    if st.button("Extract & Summarize", type="primary"):
        with st.spinner("Extracting text from PDF..."):
            extracted_text = extract_text_from_pdf(uploaded_file)
            st.session_state.extracted_text = extracted_text
            
        if "Error" in extracted_text:
            st.error(extracted_text)
        else:
            st.success("Text extracted successfully!")
            
            with st.spinner("Generating AI Summary..."):
                summary = summarize_financial_document(extracted_text)
                st.session_state.summary = summary
                
    if st.session_state.get("summary"):
        st.subheader("📝 Key Document Insights")
        st.markdown(f"""
        <div style='background-color: var(--panel); padding: 20px; border-radius: 10px; border: 1px solid var(--neon-purple); margin-top: 10px;'>
            {st.session_state.summary.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)
            
        with st.expander("View Extracted Text"):
            st.text(st.session_state.extracted_text[:3000] + "...\n\n[Text Truncated for View]")
