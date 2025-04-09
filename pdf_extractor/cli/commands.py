import sys
import os
import argparse
from typing import Optional
from tqdm import tqdm

from pdf_extractor.core.extractor import PDFExtractor


def process_pdfs(read_from: str, save_to: str, limit: Optional[int] = None) -> None:
    """
    Process all PDF files in a directory and save their extracted text.
    
    Args:
        read_from: Source directory containing PDF files
        save_to: Destination directory for extracted text files
        limit: Optional limit on the number of pages to extract per PDF
    """
    # Check if source dir exists
    if not os.path.isdir(read_from):
        print(f"Error: The source directory '{read_from}' does not exist.")
        sys.exit(1)

    # Create the output directory if it doesn't exist
    os.makedirs(save_to, exist_ok=True)

    # Get all PDF files from the source dir
    pdf_files = [file for file in os.listdir(read_from) if file.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in '{read_from}'")
        return

    extractor = PDFExtractor()
    
    # Process PDFs with enhanced progress bar
    with tqdm(
        total=len(pdf_files),
        desc="📚 Processing PDFs",
        unit="file",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]",
        ncols=80,
        colour="blue",
        position=0,
        leave=True
    ) as pbar:
        for pdf_file in pdf_files:
            pdf_path = os.path.join(read_from, pdf_file)
            
            try:
                # Extract text from the PDF
                text = extractor.extract_text(pdf_path=pdf_path, page_limit=limit)
                
                # The name before .pdf
                base_name = os.path.splitext(pdf_file)[0]
                output_file = os.path.join(save_to, f"{base_name}.txt")
                
                # Save text to file
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                # Update progress bar description with current file
                pbar.set_description(f"📚 Processing: {pdf_file}")
                pbar.update(1)
                    
            except Exception as e:
                print(f"\n❌ Failed to process {pdf_path}: {e}")
                pbar.update(1)  # Still update progress even on error

def main() -> None:
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(description='PDF Content Extractor')

    parser.add_argument(
        "--read-from",
        type=str,
        default="./files/pdf_source",
        help="Source directory containing PDF files to extract"
    )
    
    parser.add_argument(
        "--save-to",
        type=str,
        default="./files/extracted_content",
        help="Destination directory for extracted PDF content"
    )
    
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit the number of pages to extract per PDF"
    )
    
    args = parser.parse_args()

    # Process the PDFs
    process_pdfs(
        read_from=args.read_from,
        save_to=args.save_to,
        limit=args.limit
    ) 