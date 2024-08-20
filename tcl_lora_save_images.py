import os
import folder_paths  # Ensure this module is available and correctly defined
import uuid
import torch
import numpy as np
from torchvision.utils import save_image

class TclLoraSaveImages:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                "images": ("IMAGE",),  # Assume images will be provided as tensors
            },
        }

    RETURN_TYPES = ("LIST",)  # Change the return type to LIST for the paths
    RETURN_NAMES = ("image_paths",)
    FUNCTION = "process_images"
    CATEGORY = "TCL Research America"

    def process_images(self, images):
        # Define the base input directory
        base_dir = folder_paths.get_input_directory()  # Assuming this retrieves the input folder path
        
        # Create the 'resize_images' directory if it doesn't exist
        resize_dir = os.path.join(base_dir, "resize_images")
        os.makedirs(resize_dir, exist_ok=True)

        # Create a unique UUID subdirectory within 'resize_images'
        unique_dir = os.path.join(resize_dir, str(uuid.uuid4()))
        os.makedirs(unique_dir, exist_ok=True)

        # Create a list to store the paths of the resized images
        image_paths = []

        for index, keyframe in enumerate(images):
            # Save keyframe image
            if len(keyframe.shape) == 4:
                assert keyframe.shape[0] == 1
                keyframe = keyframe[0, ...]
            
            # Permute keyframe to (C, H, W)
            keyframe = keyframe.permute(2, 0, 1)

            # Extract base name and extension, and format to four digits
            output_path = os.path.join(unique_dir, f"image_{index}.png")
            save_image(keyframe, output_path)

            # Add the image path to the list
            image_paths.append(output_path)

        # Return the list of image paths
        return image_paths,