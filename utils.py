import os
import folder_paths
import uuid

def get_temp_dir():
    temp_dir = folder_paths.get_temp_directory()
    temp_dir = os.path.join(temp_dir, str(uuid.uuid4()))
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return temp_dir