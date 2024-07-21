import os
import folder_paths

def get_temp_dir():
    temp_dir = folder_paths.get_temp_directory()
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return temp_dir