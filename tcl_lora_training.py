import subprocess

class TclLoraTraining:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            'required': {
                "DATASET_CONFIG": ("STRING", {"multiline": False, "default": "/root/lora_model/datasets/80b61206-81b5-48c6-9f82-526cb473bc94/lora.toml"}),
                "OUTPUT_DIR": ("STRING", {"multiline": False, "default": "/root/lora_model/datasets/80b61206-81b5-48c6-9f82-526cb473bc94/output"}),
                "TRAINING_SET": ("STRING", {"multiline": False, "default": "80b61206-81b5-48c6-9f82-526cb473bc94"}),
                "seed": ("STRING", {"multiline": False, "default": "7697797"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("cmd",)    
    FUNCTION = "training"
    CATEGORY = "TCL Research America"

    def training(self, DATASET_CONFIG, OUTPUT_DIR, TRAINING_SET, seed):
        ckpt = "/root/workspace/ComfyUI/models/checkpoints/dreamshaperXL_v21TurboDPMSDE.safetensors"
        learning_rate = "0.0001"
        text_encoder_lr = "4e-05"
        train_batch_size = "1"
        save_every_x_epochs = "10"
        scheduler = "constant"
        num_epochs = "10"
        network_dim = "64"

        command = [
            'accelerate', 'launch',
            '--num_cpu_threads_per_process', '8', 'sdxl_train_network.py',
            '--network_module=networks.lora',
            f'--pretrained_model_name_or_path={ckpt}',
            f'--dataset_config={DATASET_CONFIG}',
            f'--output_dir={OUTPUT_DIR}',
            f'--output_name={TRAINING_SET}_last_e{num_epochs}_n{network_dim}',
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
            f'--training_comment=LORA:{TRAINING_SET}',
            '--optimizer_type=AdamW',
            '--max_data_loader_n_workers=0',
            '--masked_loss'
        ]

        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True, cwd="/root/workspace/for_weiqiang/sd-scripts-mask")
            return [command, result.stdout, result.stderr]
        except subprocess.CalledProcessError as e:
            print("Command failed with exit status:", e.returncode)
            print("Command output:", e.stderr)
            raise
        return [command, ]