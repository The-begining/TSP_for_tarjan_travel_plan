import os
import shutil
import logging
import re

class FileClassifier:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def classify_files(self, dest_dirs):
        """
        Classifies files in the base directory into corresponding destination folders.

        Args:
        - dest_dirs (dict): A dictionary mapping file patterns to destination directories.
        """
        logging.info(f"Starting file classification in {self.base_dir}")

        if not os.path.exists(self.base_dir):
            logging.error(f"Base directory {self.base_dir} does not exist.")
            return

        for file in os.listdir(self.base_dir):
            file_path = os.path.join(self.base_dir, file)

            if os.path.isfile(file_path):
                try:
                    # Match file extensions or patterns using regular expressions
                    matched = False
                    for pattern, dest_dir in dest_dirs.items():
                        if re.fullmatch(pattern, file, re.IGNORECASE):
                            os.makedirs(dest_dir, exist_ok=True)
                            new_file_path = os.path.join(dest_dir, file)
                            shutil.move(file_path, new_file_path)
                            logging.info(f"Moved {file_path} to {new_file_path}")
                            matched = True
                            break
                    
                    if not matched:
                        # Move to 'others' if no pattern matches
                        others_dir = dest_dirs.get(".others", os.path.join(self.base_dir, "others"))
                        os.makedirs(others_dir, exist_ok=True)
                        new_file_path = os.path.join(others_dir, file)
                        shutil.move(file_path, new_file_path)
                        logging.info(f"Moved {file_path} to {new_file_path}")

                except Exception as e:
                    logging.error(f"Error moving file {file}: {e}")
