import pypdf

def extract_text_from_pdf(file):
    """
    Extracts text from an uploaded PDF file.
    """
    try:
        # Create a PDF reader object
        reader = pypdf.PdfReader(file)
        
        # Extract text from each page
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() + "\n\n"
            
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"
