import os
import shutil
import folder_paths  # Ensure this module is available and correctly defined
import uuid
import torch
import numpy as np
from torchvision.utils import save_image
import logging


class TclLoraFluxGenDatasets:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                "id": ("STRING", {"multiline": False, "default": "id"}),
                "base_dir": ("STRING", {"multiline": False, "default": "id"}),
                "raw_images": ("STRING", {"multiline": True, "default": "raw_images"}),
                "raw_images_dir": ("STRING", {"multiline": False, "default": "raw_images_dir"}),
                "raw_captions": ("STRING", {"multiline": True, "default": "raw_captions"}),
                "multidatabackend": ("STRING", {"multiline": True, "default": ""}),
                "config": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING","STRING","STRING",)  # Change the return type to LIST for the paths
    RETURN_NAMES = ("dataset_config_path", "output_dir", "output_prefix",)  # Add the return names
    FUNCTION = "process_images"
    CATEGORY = "TCL Research America"

    def process_images(self, id, base_dir, raw_images, raw_images_dir, raw_captions, multidatabackend, config):
        directory = os.path.join(base_dir, id)
        if os.path.exists(directory) and os.path.isdir(directory):
            shutil.rmtree(directory)
        save_raw(raw_images, raw_images_dir, id, base_dir)
        save_caption(raw_captions, raw_images_dir, id, base_dir)
        
        output_dir = os.path.join(base_dir, id, "output")
        config_dir = os.path.join("/product-lora-script", "config")
        multidatabackend_path = os.path.join(config_dir, "multidatabackend.json")
        save_toml(multidatabackend, multidatabackend_path)
        config_path = os.path.join(config_dir, "config.json")
        save_toml(config, config_path)
        
        return config_path, output_dir, id,


def save_raw(images, path, id, base_dir):
    images_list = images.splitlines()
    for index, image in enumerate(images_list):
        os.makedirs(os.path.join(base_dir, id, path), exist_ok=True)
        shutil.copy(os.path.join("/ComfyUI/output", image), os.path.join(base_dir, id, path, f"{index:04d}.png"))

def save_caption(images, path, id, base_dir):
    images_list = images.splitlines()
    for index, caption in enumerate(images_list):
        output_path = os.path.join(base_dir, id, path, f"{index:04d}.txt")
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(caption)

def save_toml(toml, toml_path):
    with open(toml_path, 'w', encoding='utf-8') as file:
        file.write(toml)