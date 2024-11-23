import os
import pytest
from fileorganizer.file_classifier import FileClassifier


def test_file_classifier(tmp_path):
    base_dir = tmp_path / "test_dir"
    base_dir.mkdir()
    test_file = base_dir / "example.txt"
    test_file.write_text("Sample file content.")

    dest_dirs = {".txt": str(tmp_path / "text_files")}
    classifier = FileClassifier(str(base_dir))
    classifier.classify_files(dest_dirs)

    assert os.path.exists(dest_dirs[".txt"])
    assert len(os.listdir(dest_dirs[".txt"])) == 1
