import sys
import os
import argparse
from typing import Optional

from pdf_extractor.processing.worker import process_and_save_pdfs


def process_pdfs(
    read_from: str,
    save_to: str,
    single_file: str,
    limit: Optional[int] = None
) -> None:
    """
    Process all PDF files in a directory and save their extracted text.
    
    Args:
        read_from: Source directory containing PDF files
        save_to: Destination directory for extracted text files
        limit: Optional limit on the number of pages to extract per PDF
    """

    # Check if source dir exists
    if not os.path.isdir(read_from):
        print(f"Error: The source directory '{read_from}' does not exist and no file specified.")
        sys.exit(1)

    # Check if it should be batch extraction or single file extraction
    if single_file:
        pdf_path = os.path.join(read_from, single_file)
        print(f'pdf_path: {pdf_path}')
        if not os.path.isfile(pdf_path):
            print(f"Error: The specified file '{single_file}' does not exist in '{read_from}'.")
            sys.exit(1)
        pdf_files = [single_file]
    else:
        # Get all PDF files from the source dir
        pdf_files = [file for file in os.listdir(read_from) if file.lower().endswith('.pdf')]

    if not pdf_files:
        print(f"No PDF files found in '{read_from}'")
        sys.exit()

    # Create the output directory if it doesn't exist
    os.makedirs(save_to, exist_ok=True)

    process_and_save_pdfs(
        pdf_files=pdf_files,
        read_from=read_from,
        save_to=save_to,
        limit=limit
    )

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
        "--single-file",
        type=str,
        default=None,
        help="Limit to extract only the first file of a directory"
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
        single_file=args.single_file,
        limit=args.limit
    ) 