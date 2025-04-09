import sys
import os

import argparse

from pdf_extractor import extract_text_from_pdf

def main(
    read_from,
    save_to,
    limit
):
    print('Running main...')

    # Check if source dir exists
    if not os.path.isdir(read_from):
        print(f"Error: The source directory '{read_from}' does not exist.")
        sys.exit(1)

    # Create the output directory if it doesn't exist
    os.makedirs(save_to, exist_ok=True)

    # Getting all pdf files from the source dir, and filtering by the file type
    pdf_files = [ file for file in os.listdir(read_from) if file.lower().endswith('.pdf') ]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(read_from, pdf_file)        
        print(f'Processing: {pdf_path}')
        try:
            text = extract_text_from_pdf(pdf_path=pdf_path)
            # The name before .pdf
            base_name = os.path.splitext(pdf_file)[0]
            output_file = os.path.join(save_to, f"{base_name}.txt")
            # Saving file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"\nText saved to {output_file}")
        except Exception as e:
            print(f"\nFailed to extract data from the following file: {pdf_path}")

    sys.exit(1)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='PDF Content Extractor.')

    # Getting and parsing all possible args
    parser.add_argument(
        "--read-from",
        type=str,
        default="./pdf_source",
        required=False,
        help="Source path of pdfs to extract"
    )
    parser.add_argument(
        "--save-to",
        type=str,
        required=False,
        default="./extracted_destination",
        help="Destination of extracted PDF content"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        required=False,
        help="Limit of pages to extract"
    )
    args = parser.parse_args()

    # Running main
    main(
        read_from=args.read_from,
        save_to=args.save_to,
        limit=args.limit
    )