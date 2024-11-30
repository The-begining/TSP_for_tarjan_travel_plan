import os
import shutil
import logging

class FileClassifier:
    def __init__(self, base_dir=None):
        """
        Initialize the FileClassifier.

        Args:
        - base_dir (str): The base directory for classifying files. Defaults to 'outputs' in the project root.
        """
        # Dynamically set the base directory
        if base_dir is None:
            base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
        self.base_dir = base_dir

    def classify_files(self, dest_dirs):
        """
        Classify and move files in the base directory to their respective destinations.

        Args:
        - dest_dirs (dict): A mapping of file extensions to destination directories.
        """
        logging.info(f"Starting file classification in {self.base_dir}")
        for file in os.listdir(self.base_dir):
            file_path = os.path.join(self.base_dir, file)
            if os.path.isfile(file_path):
                # Extract file extension
                file_ext = os.path.splitext(file)[-1].lower()
                dest_dir = dest_dirs.get(file_ext, os.path.join(self.base_dir, "others"))
                os.makedirs(dest_dir, exist_ok=True)

                # Move file and log the action
                shutil.move(file_path, os.path.join(dest_dir, file))
                logging.info(f"Moved {file} to {dest_dir}")
