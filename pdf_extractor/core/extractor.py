import fitz
import os
from typing import Optional


class PDFExtractor:
    """
    A class for extracting text content from PDF files.
    """
    
    @staticmethod
    def extract_text(pdf_path: str, page_limit: Optional[int] = None) -> str:
        """
        Extract text from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            page_limit: Optional limit on the number of pages to extract
            
        Returns:
            Extracted text as a string
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"File '{pdf_path}' does not exist")
        
        try:
            # Open the PDF
            doc = fitz.open(pdf_path)
            
            # Determine number of pages to process
            num_pages = len(doc)
            if page_limit is not None:
                num_pages = min(num_pages, page_limit)
                
            print(f"Processing {num_pages} pages from {pdf_path}")

            # Extract text from each page
            text = ""
            for page_num in range(num_pages):
                page = doc.load_page(page_num)
                text += page.get_text()
        
            # Close the document
            doc.close()
            
            return text

        except Exception as e:
            raise RuntimeError(f"Error processing '{pdf_path}': {e}") 