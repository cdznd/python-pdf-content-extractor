import fitz
import os

def extract_text_from_pdf(pdf_path):

    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' does not exist")
        return ""
    
    try:
        # Open the PDF
        doc = fitz.open(pdf_path)

        print(f"Number of pages: {len(doc)}")

        # Extract text from each page
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
    
        # Close the document
        doc.close()
        
        return text
    
    except Exception as e:
        print(f"Error processing '{pdf_path}': {e}")
        return ""