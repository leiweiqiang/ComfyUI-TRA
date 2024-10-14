import subprocess
import os
import json
import logging
import requests
from server import PromptServer
import concurrent.futures
import threading
import queue
import re
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CheckpointHandler(FileSystemEventHandler):
    """Handler for checkpoint file creation events."""
    def __init__(self, callback):
        self.callback = callback

    def on_created(self, event):
        """Called when a file is created in the monitored directory."""
        if not event.is_directory and event.src_path.endswith('.safetensors'):
            self.callback(f"Saving checkpoint: {event.src_path}")

class TclLoraFluxTraining:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.prompt_server = PromptServer.instance
        self.api_url = "https://minestudio.tcl-research.us/api/lora_training_log"
        self.prompt_id = ""
        self.observer = None
        self.monitoring = False

    @classmethod
    def INPUT_TYPES(s):
        """Define input types for the ComfyUI node."""
        return {
            "required": {
                "DATASET_CONFIG": ("STRING", {"multiline": False, "default": "/root/lora_model/datasets/80b61206-81b5-48c6-9f82-526cb473bc94/lora.toml"}),
                "OUTPUT_DIR": ("STRING", {"multiline": False, "default": "/root/lora_model/datasets/80b61206-81b5-48c6-9f82-526cb473bc94/output"}),
                "TRAINING_SET": ("STRING", {"multiline": False, "default": "80b61206-81b5-48c6-9f82-526cb473bc94"}),
                "seed": ("STRING", {"multiline": False, "default": "7697797"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)    
    FUNCTION = "training"
    CATEGORY = "TCL Research America"

    def log(self, message, level="info"):
        """Log a message and send it to the prompt server and API."""
        if level == "info":
            self.logger.info(message)
        elif level == "error":
            self.logger.error(message)
        elif level == "warning":
            self.logger.warning(message)
        
        data = {
            "message": message,
            "level": level,
            "name": "LORA_Training",
            "prompt_id": self.prompt_id
        }
        self.prompt_server.send_sync("lora_training_log", data)
        # Send the log data asynchronously
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self.send_log_data, data)

    def send_log_data(self, data):
        """Send log data to the API."""
        try:
            response = requests.post(self.api_url, json=data)
            if response.status_code != 200:
                self.logger.error(f"Failed to send log data: {response.status_code} - {response.text}")
        except Exception as e:
            self.logger.error(f"Error sending log data: {str(e)}")

    def ensure_directory_exists(self, directory):
        """Ensure that the specified directory exists, creating it if necessary."""
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                self.log(f"Created output directory: {directory}")
            except Exception as e:
                self.log(f"Error creating output directory {directory}: {str(e)}", level="error")
                return False
        return True

    def start_file_monitoring(self, directory):
        """Start monitoring the specified directory for new checkpoint files."""
        if not self.ensure_directory_exists(directory):
            return False

        try:
            event_handler = CheckpointHandler(self.log)
            self.observer = Observer()
            self.observer.schedule(event_handler, directory, recursive=True)
            self.observer.start()
            self.monitoring = True
            self.log(f"Started file monitoring in {directory}")
            return True
        except Exception as e:
            self.log(f"Error starting file monitoring: {str(e)}", level="error")
            return False

    def stop_file_monitoring(self):
        """Stop the file monitoring process."""
        if self.observer and self.monitoring:
            try:
                self.observer.stop()
                self.observer.join()
                self.monitoring = False
                self.log("Stopped file monitoring")
            except Exception as e:
                self.log(f"Error stopping file monitoring: {str(e)}", level="error")
        else:
            self.log("File monitoring was not active", level="warning")

    def process_output(self, process):
        """Process the output of the training subprocess."""
        progress_patterns = [
            re.compile(r'(\d+%|\d+/\d+|\d+\.\d+/\d+\.\d+)'),  # Percentage or step progress
            re.compile(r'Epoch \d+/\d+'),                     # Epoch progress
            re.compile(r'Step \d+/\d+'),                      # Step progress
            re.compile(r'Loss: \d+\.\d+'),                    # Loss information
            re.compile(r'Saving model'),                      # Model saving indication
            re.compile(r'(\w+): \d+\.\d+')                    # Any metric in format "MetricName: Value"
        ]
        
        def read_stream(stream, level):
            """Read from a stream and log the output."""
            for line in iter(stream.readline, ''):
                line = line.strip()
                if line:
                    progress_found = any(pattern.search(line) for pattern in progress_patterns)
                    
                    if progress_found:
                        self.log(f"Progress: {line}", level="info")
                    else:
                        self.log(line, level=level)

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(read_stream, process.stdout, "info")
            executor.submit(read_stream, process.stderr, "error")

        process.wait()


    def training(self, DATASET_CONFIG, OUTPUT_DIR, TRAINING_SET, seed):
        self.prompt_id = TRAINING_SET

        command = [
            'bash', 'train.sh'
        ]

        self.log(f"Starting LoRA Flux training with command: {' '.join(command)}")

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd="/product-lora-script"
            )
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.log(output.strip())
            
            return_code = process.poll()
            
            if return_code == 0:
                # self.log("LoRA Flux training completed successfully")
                return ("Training completed successfully",)
            else:
                # self.log(f"LoRA Flux training failed with return code {return_code}", level="error")
                return (f"Training failed with return code {return_code}",)
        
        except Exception as e:
            # self.log(f"An error occurred during LoRA Flux training: {str(e)}", level="error")
            return (f"Error occurred: {str(e)}",)