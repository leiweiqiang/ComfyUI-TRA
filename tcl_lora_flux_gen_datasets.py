import os
import shutil
import folder_paths  # Ensure this module is available and correctly defined
import uuid
import torch
import numpy as np
from torchvision.utils import save_image
import logging
import toml
import json


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
        save_json(multidatabackend, multidatabackend_path)
        config_path = os.path.join(config_dir, "config.env")
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

def save_toml(data, toml_path):
    toml_dict = {}
    for line in data.split('\n'):
        if line.startswith('export '):
            key, value = line[7:].split('=', 1)
            toml_dict[key] = value.strip("'")
    
    with open(toml_path, 'w', encoding='utf-8') as file:
        toml.dump(toml_dict, file)

def save_json(json_string, file_path):
    try:
        json_string = json_string.strip('"').encode().decode('unicode_escape')
        data = json.loads(json_string)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
        print(f"Formatted JSON successfully saved to {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except IOError as e:
        print(f"Error writing to file: {e}")    