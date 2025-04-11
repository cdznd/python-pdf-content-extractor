import os

def save_text_to_file(pdf_file: str, save_to: str, text: str):
    # The name before .pdf
    base_name = os.path.splitext(pdf_file)[0]
    output_file = os.path.join(save_to, f"{base_name}.txt")
                
    # Save text to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)