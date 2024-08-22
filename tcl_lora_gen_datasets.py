import os
import folder_paths  # Ensure this module is available and correctly defined
import uuid
import torch
import numpy as np
from torchvision.utils import save_image

class TclLoraGenDatasets:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                "raw_images": ("STRING", {"multiline": True, "default": "raw_images"}),
                "raw_images_dir": ("STRING", {"multiline": False, "default": "raw_images_dir"}),
                "raw_masks": ("STRING", {"multiline": True, "default": "raw_masks"}),
                "raw_masks_dir": ("STRING", {"multiline": False, "default": "raw_masks_dir"}),
                "raw_captions": ("STRING", {"multiline": True, "default": "raw_captions"}),
                "reg_images": ("STRING", {"multiline": True, "default": "reg_images"}),
                "reg_images_dir": ("STRING", {"multiline": False, "default": "reg_images_dir"}),
                "reg_masks": ("STRING", {"multiline": True, "default": "reg_masks"}),
                "reg_masks_dir": ("STRING", {"multiline": False, "default": "reg_masks_dir"}),
                "reg_captions": ("STRING", {"multiline": True, "default": "reg_captions"}),
            },
        }

    RETURN_TYPES = ("STRING",)  # Change the return type to LIST for the paths
    RETURN_NAMES = ("help",)
    FUNCTION = "process_images"
    CATEGORY = "TCL Research America"

    def process_images(self, raw_images, raw_images_dir, raw_masks, raw_masks_dir, raw_captions, reg_images, reg_images_dir, reg_masks, reg_masks_dir, reg_captions):
        
        return "success",