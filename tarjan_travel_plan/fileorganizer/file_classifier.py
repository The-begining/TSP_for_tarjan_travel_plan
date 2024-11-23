import os
import shutil


class FileClassifier:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def classify_files(self, dest_dirs):
        for file in os.listdir(self.base_dir):
            file_path = os.path.join(self.base_dir, file)
            if os.path.isfile(file_path):
                file_ext = os.path.splitext(file)[-1].lower()
                dest_dir = dest_dirs.get(file_ext, os.path.join(self.base_dir, "others"))
                os.makedirs(dest_dir, exist_ok=True)
                shutil.move(file_path, os.path.join(dest_dir, file))
