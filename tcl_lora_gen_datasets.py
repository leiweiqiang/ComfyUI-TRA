import os
import shutil
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
                "id": ("STRING", {"multiline": False, "default": "id"}),
                "base_dir": ("STRING", {"multiline": False, "default": "id"}),
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
                "toml": ("STRING", {"multiline": True, "default": "toml"}),
            },
        }

    RETURN_TYPES = ("STRING",)  # Change the return type to LIST for the paths
    RETURN_NAMES = ("help",)
    FUNCTION = "process_images"
    CATEGORY = "TCL Research America"

    def process_images(self, id, base_dir, raw_images, raw_images_dir, raw_masks, raw_masks_dir, raw_captions, reg_images, reg_images_dir, reg_masks, reg_masks_dir, reg_captions, toml):
        directory = os.path.join(folder_paths.get_output_directory(), base_dir, id)
        if os.path.exists(directory) and os.path.isdir(directory):
            shutil.rmtree(directory)
        save_raw(raw_images, raw_images_dir, id, base_dir)
        save_reg(raw_masks, raw_masks_dir, id, base_dir)
        save_caption(raw_captions, raw_images_dir, id, base_dir)
        save_raw(reg_images, reg_images_dir, id, base_dir)
        save_reg(reg_masks, reg_masks_dir, id, base_dir)
        save_caption(reg_captions, reg_images_dir, id, base_dir)
        save_toml(toml, reg_images_dir, id, base_dir)
        return "success",

def save_raw(images, path, id, base_dir):
    images_list = images.splitlines()
    for index, image in enumerate(images_list):
        os.makedirs(os.path.join(folder_paths.get_output_directory(), base_dir, id, path), exist_ok=True)
        shutil.copy(os.path.join(folder_paths.get_output_directory(), image), os.path.join(folder_paths.get_output_directory(), base_dir, id, path, f"{index:04d}.png"))

def save_reg(images, path, id, base_dir):
    images_list = images.splitlines()
    for index, image in enumerate(images_list):
        os.makedirs(os.path.join(folder_paths.get_output_directory(), base_dir, id, path), exist_ok=True)
        shutil.copy(os.path.join(folder_paths.get_output_directory(), image), os.path.join(folder_paths.get_output_directory(), base_dir, id, path, f"{index:04d}.png"))

def save_caption(images, path, id, base_dir):
    images_list = images.splitlines()
    for index, caption in enumerate(images_list):
        output_path = os.path.join(folder_paths.get_output_directory(), base_dir, id, path, f"{index:04d}.txt")
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(caption)

def save_toml(toml, path, id, base_dir):
    output_path = os.path.join(folder_paths.get_output_directory(), base_dir, id, f"lora.toml")
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(toml)