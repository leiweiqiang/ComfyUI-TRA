import subprocess
import yaml
import os
import json
import logging
import requests
from server import PromptServer
import concurrent.futures

class TclFrescoWrapedNoise:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            'required': {
                "model_type": (["XL", "kolors"],),
                "controlnet_strength": ("FLOAT", {"default": 0.7, "min": 0.7, "max": 1.0}),
                "ip_adapter_scale": ("FLOAT", {"default": 0.3, "min": 0.3, "max": 0.9}),
                "max_images": ("INT", {"default": 3, "min": 3, "max": 200}),
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "negative": ("STRING", {"multiline": True, "default": ""}),
                "video_path": ("STRING", {"multiline": False, "default": "/workspace/FRESCO-wraped-noise/data/example/video_square.mp4"}),
                "save_path": ("STRING", {"multiline": False, "default": "/workspace/FRESCO-wraped-noise/output888"}),
                "ref_img_ip_adapter": ("STRING", {"multiline": False, "default": "/workspace/FRESCO-wraped-noise/data/example/ref_img.png"}),
                "noise_type": ("STRING", {"multiline": False, "default": "integral"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("help",)
    FUNCTION = "fresco"
    OUTPUT_NODE = False
    CATEGORY = "TCL Research America"

import subprocess
import yaml
import os
import json
import logging
import requests
from server import PromptServer
import concurrent.futures

class TclFrescoWrapedNoise:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.prompt_server = PromptServer.instance
        self.api_url = "https://minestudio.tcl-research.us/api/lora_training_log"
        self.prompt_id = ""

    @classmethod
    def INPUT_TYPES(s):
        return {
            'required': {
                "model_type": (["XL", "kolors"],),
                "controlnet_strength": ("FLOAT", {"default": 0.7, "min": 0.7, "max": 1.0}),
                "ip_adapter_scale": ("FLOAT", {"default": 0.3, "min": 0.3, "max": 0.9}),
                "max_images": ("INT", {"default": 3, "min": 3, "max": 200}),
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "negative": ("STRING", {"multiline": True, "default": ""}),
                "video_path": ("STRING", {"multiline": False, "default": "/workspace/FRESCO-wraped-noise/data/example/video_square.mp4"}),
                "save_path": ("STRING", {"multiline": False, "default": "/workspace/FRESCO-wraped-noise/output888"}),
                "ref_img_ip_adapter": ("STRING", {"multiline": False, "default": "/workspace/FRESCO-wraped-noise/data/example/ref_img.png"}),
                "noise_type": ("STRING", {"multiline": False, "default": "integral"}),
                "prompt_id": ("STRING", {"multiline": False, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("help",)
    FUNCTION = "fresco"
    OUTPUT_NODE = False
    CATEGORY = "TCL Research America"

    def log(self, message, level="info"):
        if level == "info":
            self.logger.info(message)
        elif level == "error":
            self.logger.error(message)
        elif level == "warning":
            self.logger.warning(message)
        
        data = {
            "message": message,
            "level": level
        }
        self.prompt_server.send_sync("lora_training_log", data)

        # Send the log data asynchronously
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self.send_log_data, {"prompt_id": self.prompt_id, "message": message, "level": level})

    def send_log_data(self, data):
        try:
            response = requests.post(self.api_url, json=data)
            if response.status_code != 200:
                # self.logger.info("Log data sent successfully")
            # else:
                self.logger.error(f"Failed to send log data: {response.status_code} - {response.text}")
        except Exception as e:
            self.logger.error(f"Error sending log data: {str(e)}")


    def fresco(self, model_type, controlnet_strength, ip_adapter_scale, max_images, prompt, negative, video_path, save_path, ref_img_ip_adapter, noise_type, prompt_id):
        self.prompt_id = prompt_id
        # Define the base YAML configurations
        yaml_data = {
            "kolors": {
                "sd_path": "./model/Kolors/",
                "model_type": "kolors",
                "guidance_scale": 7.5,
                "use_controlnet": True,
                "controlnet_path": "canny-kolors",
                "controlnet_type": "canny-kolors",
                "controlnet_strength": 1.0,
                "num_inference_steps": 50,
                "video_path": "./data/example/video_square.mp4",
                "save_path": "./output/test/kolors",
                "mininterv": 10,
                "maxinterv": 10,
                "max_images": 3,
                "prompt": "A beautiful photograph of a french street, straight-on 600mm telephoto lens shot f/32",
                "negative": "(blurry, out of focus, unclear, depth of field, indistinct, 35mm, bokeh, blurred background, blurred foreground, blurred subject, hazy, foggy, washed out, fuzzy, faint)",
                "batch_size": 3,
                "ip_adapter_name": "ip_adapter_plus_general.bin",
                "ip_adapter_scale": 0.8,
                "ref_img_ip_adapter": "./data/example/ref_img.png",
                "use_saliency": False,
                "end_opt_step": 45,
                "seed": 0,
                "img_size": 1024,
                "scheduler": "DDPMScheduler",
                "intra_weight": 0.0,
                "strength": 0.6,
                "noise_type": "integral"
            },
            "XL": {
                "sd_path": "./model/checkpoints/juggernautXL_v9Rundiffusionphoto2.safetensors",
                "model_type": "XL",
                "guidance_scale": 7.5,
                "use_controlnet": True,
                "controlnet_path": "canny-xl",
                "controlnet_type": "canny-xl",
                "controlnet_strength": 1.0,
                "num_inference_steps": 35,
                "video_path": "./data/example/video_square.mp4",
                "save_path": "./output/test/XL",
                "mininterv": 10,
                "maxinterv": 10,
                "max_images": 3,
                "prompt": "A beautiful  photograph of a french street, cinematic, hyperdetailed photograph, shiny scales, 8k resolution,",
                "negative": "(worst quality, low quality, normal quality, lowres, low details, oversaturated, undersaturated, overexposed, underexposed, grayscale, bw, bad photo, bad photography, bad art:1.4), (watermark, signature, text font, username, error, logo, words, letters, digits, autograph, trademark, name:1.2), (blur, blurry, grainy), morbid, ugly, asymmetrical, mutated malformed, mutilated, poorly lit, bad shadow, draft, cropped, out of frame, cut off, censored, jpeg artifacts, out of focus, glitch, duplicate, (airbrushed, cartoon, anime, semi-realistic, cgi, render, blender, digital art, manga, amateur:1.3), (3D ,3D Game, 3D Game Scene, 3D Character:1.1), (bad hands, bad anatomy, bad body, bad face, bad teeth, bad arms, bad legs, deformities:1.3)",
                "batch_size": 3,
                "use_saliency": True,
                "end_opt_step": 30,
                "seed": 0,
                "img_size": 1024,
                "scheduler": "DDPMScheduler",
                "ip_adapter_name": "ip-adapter_sdxl.safetensors",
                "ip_adapter_scale": 0.8,
                "ref_img_ip_adapter": "./data/example/ref_img.png",
                "strength": 0.85,
                "noise_type": "integral"
            }
        }

        # Select the correct YAML data based on model_type
        config = yaml_data.get(model_type)

        # Replace values based on the input parameters
        if config:
            config['controlnet_strength'] = controlnet_strength
            config['ip_adapter_scale'] = ip_adapter_scale
            config['max_images'] = max_images
            config['prompt'] = prompt
            config['negative'] = negative
            config['video_path'] = video_path
            config['save_path'] = f"/workspace/ComfyUI/output/{save_path}"
            config['ref_img_ip_adapter'] = ref_img_ip_adapter
            config['noise_type'] = noise_type

        # Define the path where the config file will be saved
        config_path = f"/workspace/ComfyUI/input/config_{model_type}.yaml"

        # Save the final configuration to a YAML file
        with open(config_path, 'w') as yaml_file:
            yaml.dump(config, yaml_file)

        # Run the Python script using the saved config file, after activating the virtual environment
        command = f"PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512 python /workspace/FRESCO-wraped-noise/run_fresco_updated.py --config_path {config_path}"
        # subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd="/workspace/FRESCO-wraped-noise")
        self.log(f"Starting Fresco Wraped Noise training with command: {command}")

        if os.path.exists(config_path):
            self.log(f"file {config_path} exist")
        else:
            self.log(f"file {config_path} not exist")

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd="/workspace/FRESCO-wraped-noise"
            )
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.log(output.strip())
            
            return_code = process.poll()
            
            if return_code == 0:
                self.log("LORA training completed successfully")
                return ("Training completed successfully",)
            else:
                self.log(f"LORA training failed with return code {return_code}", level="error")
                return (f"Training failed with return code {return_code}",)
        
        except Exception as e:
            self.log(f"An error occurred during LORA training: {str(e)}", level="error")
            return (f"Error occurred: {str(e)}",)
                

