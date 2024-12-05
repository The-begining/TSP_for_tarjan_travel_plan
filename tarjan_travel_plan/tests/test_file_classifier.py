import os
import pytest
from tarjan_travel_plan.fileorganizer.file_classifier import FileClassifier


def test_file_classifier(tmp_path):
    # Setup
    base_dir = tmp_path / "test_dir"
    base_dir.mkdir()
    test_file = base_dir / "example.txt"
    test_file.write_text("Sample file content.")

    # Destination directories
    dest_dirs = {r".*\.txt$": str(tmp_path / "text_files")}

    # Run classification
    classifier = FileClassifier(str(base_dir))
    classifier.classify_files(dest_dirs)

    # Debug: Use the correct regex key to access the destination directory
    regex_key = r".*\.txt$"
    dest_dir_path = dest_dirs[regex_key]
    print(f"Destination directory path: {dest_dir_path}")
    print(f"Files in destination: {os.listdir(dest_dir_path) if os.path.exists(dest_dir_path) else 'Destination not created!'}")

    # Verify
    assert os.path.exists(dest_dir_path), "Destination directory was not created."
    assert os.path.exists(os.path.join(dest_dir_path, "example.txt")), "File was not moved to the destination directory."
