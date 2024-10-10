import os
import subprocess

class TclLoraCheckPoints:
    
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            'required': {
                'ID': ("STRING", {"multiline": False, "default": ""}),
                'seed': ("STRING", {"multiline": False, "default": ""}),
            },
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("checkpoints",)    
    FUNCTION = "checkpoints"
    CATEGORY = "TCL Research America"

    def checkpoints(self, ID, seed):
        files_and_dirs = list_file_names_in_directory(os.path.join("/ComfyUI/input/LoRA_Training_Datasets", ID, "output"))
        ln_create(files_and_dirs, ID)
        return [files_and_dirs,]

def list_file_names_in_directory(directory):
    try:
        files_and_dirs = os.listdir(directory)
        file_names = [f for f in files_and_dirs if os.path.isfile(os.path.join(directory, f))]
        return sorted(file_names)
    except FileNotFoundError:
        return []
    except Exception as e:
        return []

def ln_create(file_names, ID):
    for file in file_names:
        src_path = f'/ComfyUI/input/LoRA_Training_Datasets/{ID}/output/{file}'
        dest_path = f'/ComfyUI/output/{file}'
        if not os.path.exists(dest_path):
            command = ['ln', '-s', src_path, dest_path]