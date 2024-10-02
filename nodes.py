from .tcl_lora_save_images import TclLoraSaveImages
from .tcl_lora_gen_datasets import TclLoraGenDatasets
from .tcl_lora_training import TclLoraTraining
from .tcl_lora_checkpoints import TclLoraCheckpoints

NODE_CLASS_MAPPINGS = {
    "TclLoraSaveImages":TclLoraSaveImages,
    "TclLoraGenDatasets":TclLoraGenDatasets,
    "TclLoraTraining":TclLoraTraining,
    "TclLoraCheckpoints":TclLoraCheckpoints
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "TclLoraSaveImages": "TCL Lora Save Images",
    "TclLoraGenDatasets":"TCL Lora Gen Datasets",
    "TclLoraTraining":"TCL Lora Training",
    "TclLoraCheckpoints":"TCL Lora Checkpoints"
}
