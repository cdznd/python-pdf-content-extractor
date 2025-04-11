import os
from tqdm import tqdm
from pdf_extractor.core.extractor import PDFExtractor
from pdf_extractor.processing.utils import save_text_to_file

# Process PDFs with enhanced progress bar
def process_and_save_pdfs(pdf_files, read_from, save_to, limit):
    extractor = PDFExtractor()

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

                save_text_to_file(
                    pdf_file,
                    save_to,
                    text
                )

                # Update progress bar description with current file
                pbar.set_description(f"📚 Processing: {pdf_file}")
                pbar.update(1)
                    
            except Exception as e:
                print(f"\n❌ Failed to process {pdf_path}: {e}")
                pbar.update(1)  # Still update progress even on error