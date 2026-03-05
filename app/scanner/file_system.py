"""
This module is used to scan the file system for files with a given extension.
Purpose: The "Eyes." This finds the files you want to audit.
"""

import os

def get_all_files(directory: str, extension: str = ".rb"):
    """Finds all files (defaulting to Ruby for your Rails background)."""
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                file_list.append(os.path.join(root, file))
    return file_list

def read_file(file_path: str):
    with open(file_path, "r") as f:
        return f.read()