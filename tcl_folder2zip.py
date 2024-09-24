import os
import subprocess

class TclFolder2Zip:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            'required': {
                "subfolder": ("STRING", {"multiline": False, "default": ""}),
                "type": ("STRING", {"multiline": False, "default": "output"}),
            },
        }

    RETURN_TYPES = ("JSON",)
    RETURN_NAMES = ("output",)    
    FUNCTION = "process"
    CATEGORY = "TCL Research America"

    def process(self, subfolder, type):
        output_file = os.path.join("/root/workspace/ComfyUI/output", f"{subfolder}.zip")
        folder = os.path.join("/root/workspace/ComfyUI", type, subfolder)
        command = ["zip", "-r", output_file, folder]
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return {
            "filename": os.path.basename(output_file),
            "subfolder":"",
            "type":"output"
        },