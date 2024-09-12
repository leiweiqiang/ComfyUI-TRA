import uuid
from .greenscreen_utils import greenscreen_removal
import logging

class TclRelighting:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            'required': {
                "keyframes": ("LIST",),
            },
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("output",)    
    FUNCTION = "process"
    CATEGORY = "TCL Research America"

    def process(self, keyframes):
        subfolder = str(uuid.uuid4())
        output = []
        for index, keyframe in enumerate(keyframes):
            result = greenscreen_removal(keyframe, subfolder)
            logging.info(result)
            output.append(result)

        return output,
