class TclLoraTraining:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            'required': {
                'DATASET_CONFIG': ("STRING", {"multiline": False, "default": ""}),
                "OUTPUT_DIR": ("PATH",),
                'TRAINING_SET': ("STRING", {"multiline": False, "default": ""}),
            },
        }

    FUNCTION = "training"
    OUTPUT_NODE = False
    CATEGORY = "TCL Research America"

    def training(self, DATASET_CONFIG, OUTPUT_DIR, TRAINING_SET):
        ckpt = "/root/workspace/ComfyUI/models/checkpoints/dreamshaperXL_v21TurboDPMSDE.safetensors" 
        learning_rate="0.0001"
        text_encoder_lr="4e-05"
        train_batch_size="1"
        save_every_x_epochs="10"
        scheduler="constant"
        num_epochs="1000"
        network_dim="64"

        command = ['ebsynthcmd', 'launch']
        command += ['--num_cpu_threads_per_process', '8', 'sdxl_train_network.py']
        command += ['--network_module="networks.lora"']
        command += [f'--pretrained_model_name_or_path="{ckpt}"']
        command += [f'--dataset_config="{DATASET_CONFIG}"']
        command += [f'--output_dir="{OUTPUT_DIR}"']
        command += [f'--output_name="{TRAINING_SET}_last_e{num_epochs}_n{network_dim}"']
        command += ['--caption_extension=".txt"']
        command += ['--prior_loss_weight=1']
        command += ['--network_alpha=16']
        command += ['--resolution=1024']
        command += [f'--train_batch_size="{train_batch_size}"']
        command += [f'--learning_rate="{learning_rate}"']
        command += [f'--unet_lr="{learning_rate}"']
        command += [f'--text_encoder_lr="{text_encoder_lr}"']
        command += [f'--max_train_epochs="100"']
        command += ['--mixed_precision="bf16"']
        command += ['--save_precision="bf16"']
        command += ['--xformers']
        command += [f'--save_every_n_epochs="{save_every_x_epochs}"']
        command += ['--save_model_as=safetensors']
        command += ['--seed=7']
        command += ['--no_half_vae']
        command += ['--color_aug']
        command += [f'--network_dim="128"']
        command += [f'--lr_scheduler="{scheduler}"']
        command += [f'--training_comment="LORA:{TRAINING_SET}"']
        command += ['--optimizer_type="AdamW"']
        command += ['--max_data_loader_n_workers="0"']
        command += ['--masked_loss']

        return 