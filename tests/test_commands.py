import os
import sys
import pytest
from unittest.mock import patch

# Assuming your function is in a file named pdf_processor.py
from pdf_extractor.cli.commands import process_pdfs

@pytest.fixture
def setup_dirs(tmp_path): # Using tmp_path pytest built in fixture
    read_from = tmp_path / "input"
    save_to = tmp_path / "output"
    read_from.mkdir()
    return str(read_from), str(save_to)

def test_source_dir_not_exist(tmp_path):
    fake_dir = tmp_path / "nonexistent"
    with pytest.raises(SystemExit), patch("builtins.print") as mock_print:
        process_pdfs(str(fake_dir), "some/output", single_file="", limit=None)
        mock_print.assert_called_with(f"Error: The source directory '{fake_dir}' does not exist and no file specified.")

def test_single_file_not_found(setup_dirs):
    read_from, save_to = setup_dirs
    with pytest.raises(SystemExit), patch("builtins.print") as mock_print:
        process_pdfs(read_from, save_to, single_file="missing.pdf")
        mock_print.assert_called_with(
            f"Error: The specified file 'missing.pdf' does not exist in '{read_from}'."
        )

def test_no_pdfs_found(setup_dirs):
    read_from, save_to = setup_dirs
    with pytest.raises(SystemExit), patch("builtins.print") as mock_print:
        process_pdfs(read_from, save_to, single_file="")
        mock_print.assert_called_with(f"No PDF files found in '{read_from}'")

def test_single_pdf_file_processed(setup_dirs):
    read_from, save_to = setup_dirs
    sample_file = "doc.pdf"
    file_path = os.path.join(read_from, sample_file)
    with open(file_path, "w") as f:
        f.write("dummy")

    with patch("pdf_extractor.cli.commands.process_and_save_pdfs") as mock_process:
        process_pdfs(read_from, save_to, single_file=sample_file, limit=2)
        mock_process.assert_called_once_with(
            pdf_files=[sample_file],
            read_from=read_from,
            save_to=save_to,
            limit=2
        )

def test_batch_pdf_files_processed(setup_dirs):
    read_from, save_to = setup_dirs
    for name in ["a.pdf", "b.PDF", "c.txt"]:
        with open(os.path.join(read_from, name), "w") as f:
            f.write("dummy")

    with patch("pdf_extractor.cli.commands.process_and_save_pdfs") as mock_process:
        process_pdfs(read_from, save_to, single_file="", limit=None)
        mock_process.assert_called_once_with(
            pdf_files=["a.pdf", "b.PDF"],
            read_from=read_from,
            save_to=save_to,
            limit=None
        )
