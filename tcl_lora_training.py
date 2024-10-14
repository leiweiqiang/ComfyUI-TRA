import subprocess
import os
import json
import logging
import requests
from server import PromptServer
import concurrent.futures

class TclLoraTraining:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.prompt_server = PromptServer.instance
        self.api_url = "https://minestudio.tcl-research.us/api/lora_training_log"
        self.prompt_id = ""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "DATASET_CONFIG": ("STRING", {"multiline": False, "default": "/root/lora_model/datasets/80b61206-81b5-48c6-9f82-526cb473bc94/lora.toml"}),
                "OUTPUT_DIR": ("STRING", {"multiline": False, "default": "/root/lora_model/datasets/80b61206-81b5-48c6-9f82-526cb473bc94/output"}),
                "TRAINING_SET": ("STRING", {"multiline": False, "default": "80b61206-81b5-48c6-9f82-526cb473bc94"}),
                "learning_rate": ("STRING", {"multiline": False, "default": "0.0001"}),
                "train_batch_size": ("STRING", {"multiline": False, "default": "1"}),
                "num_epochs": ("STRING", {"multiline": False, "default": "100"}),
                "save_every_x_epochs": ("STRING", {"multiline": False, "default": "10"}),
                "output_name_prefix": ("STRING", {"multiline": False, "default": "80b61206-81b5-48c6-9f82-526cb473bc94"}),
                "seed": ("STRING", {"multiline": False, "default": "7697797"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)    
    FUNCTION = "training"
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

    def training(self, DATASET_CONFIG, OUTPUT_DIR, TRAINING_SET, learning_rate, train_batch_size, num_epochs, save_every_x_epochs, output_name_prefix, seed):
        ckpt = "/ComfyUI/models/checkpoints/dreamshaperXL_v21TurboDPMSDE.safetensors"
        # learning_rate = "0.0001"
        text_encoder_lr = "4e-05"
        # train_batch_size = "1"
        # save_every_x_epochs = "10"
        scheduler = "constant"
        # num_epochs = "10"
        network_dim = "64"
        self.prompt_id = TRAINING_SET

        command = [
            'accelerate', 'launch',
            '--num_cpu_threads_per_process', '8', 'sdxl_train_network.py',
            '--network_module=networks.lora',
            f'--pretrained_model_name_or_path={ckpt}',
            f'--dataset_config={DATASET_CONFIG}',
            f'--output_dir={OUTPUT_DIR}',
            f'--output_name={output_name_prefix}_last_e{num_epochs}_n{network_dim}',
            '--caption_extension=.txt',
            '--prior_loss_weight=1',
            '--network_alpha=16',
            '--resolution=1024',
            f'--train_batch_size={train_batch_size}',
            f'--learning_rate={learning_rate}',
            f'--unet_lr={learning_rate}',
            f'--text_encoder_lr={text_encoder_lr}',
            f'--max_train_epochs={num_epochs}',
            '--mixed_precision=bf16',
            '--save_precision=bf16',
            '--xformers',
            f'--save_every_n_epochs={save_every_x_epochs}',
            '--save_model_as=safetensors',
            f'--seed={seed}',
            '--no_half_vae',
            '--color_aug',
            f'--network_dim={network_dim}',
            f'--lr_scheduler={scheduler}',
            f'--training_comment=LORA:{output_name_prefix}',
            '--optimizer_type=AdamW',
            '--max_data_loader_n_workers=0',
            '--masked_loss'
        ]

        self.log(f"Starting LORA training with command: {' '.join(command)}")

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd="/sd-scripts-mask"
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