import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

# Use the recommended model for chat
MODEL_NAME = "gemini-1.5-flash"

def get_gemini_model():
    """Returns the Gemini GenerativeModel instance configured with system instructions."""
    system_instruction = (
        "You are an expert AI Personal Finance Assistant. "
        "Your goal is to help the user with budgeting, saving, investments, taxes, EMI, and general financial planning. "
        "Provide direct, helpful, and professional advice. "
        "Keep your tone encouraging and easily understandable for people without a finance background. "
        "Important rule: Always append a short disclaimer to your advice that you are an AI and your guidance is for informational purposes only, not formal financial advice."
    )
    
    return genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=system_instruction
    )

def generate_chat_response(messages):
    """
    Generates a response from the model given the message history.
    Streamlit session_state stores messages as dicts: {"role": "user"/"assistant", "content": "..."}
    Gemini expects: [{"role": "user"/"model", "parts": ["..."]}]
    """
    if not API_KEY:
        return "Error: Gemini API key not found. Please add it to your .env file or Streamlit secrets."
        
    try:
        model = get_gemini_model()
        
        # Convert streamlit messages to Gemini history format
        # Note: Gemini history format is role: user or model
        history = []
        for msg in messages[:-1]: # exclude the last user message
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": [msg["content"]]})
            
        # Start chat with history
        chat = model.start_chat(history=history)
        
        # Send the latest message
        latest_message = messages[-1]["content"]
        response = chat.send_message(latest_message)
        
        return response.text
    except Exception as e:
        return f"An error occurred while generating a response: {str(e)}"

def analyze_financial_data(data_summary):
    """Generates financial insights based on a summary of spending data."""
    if not API_KEY:
        return "Error: Gemini API key not found."
        
    try:
        prompt = f"""
        As a financial advisor, analyze the following monthly spending breakdown and provide 
        3 actionable tips for saving money or optimizing these expenses. 
        Keep the response concise and use bullet points.

        Data:
        {data_summary}
        """
        model = genai.GenerativeModel(model_name=MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

def summarize_financial_document(text):
    """Summarizes extracted text from a PDF financial document."""
    if not API_KEY:
        return "Error: Gemini API key not found."
    
    try:
        prompt = f"""
        You are an expert financial analyst. Please summarize the following financial document text.
        Focus on extracting:
        1. Key financial figures (revenues, expenses, totals, balances, returns).
        2. Important dates, terms, or conditions.
        3. A brief summary of the overall document's purpose.

        Document Text:
        {text[:20000]} # Limit text length to avoid token limits for large PDFs
        """
        model = genai.GenerativeModel(model_name=MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"
