from .ComfyUI.greenscreen_utils import greenscreen_removal

class TclExr2png:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            'required': {
                "filename": ("STRING", {"multiline": False, "default": ""}),
                "subfolder": ("STRING", {"multiline": False, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output",)    
    FUNCTION = "process"
    CATEGORY = "TCL Research America"

    def process(self, filename, subfolder):
        return greenscreen_removal(filename, subfolder),