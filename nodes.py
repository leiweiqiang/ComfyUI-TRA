from .tcl_lora_save_images import TclLoraSaveImages
from .tcl_lora_gen_datasets import TclLoraGenDatasets
from .tcl_lora_training import TclLoraTraining
from .tcl_lora_flux_gen_datasets import TclLoraFluxGenDatasets
from .tcl_lora_flux_training import TclLoraFluxTraining
from .tcl_lora_checkpoints import TclLoraCheckPoints

NODE_CLASS_MAPPINGS = {
    "TclLoraSaveImages":TclLoraSaveImages,
    "TclLoraGenDatasets":TclLoraGenDatasets,
    "TclLoraTraining":TclLoraTraining,
    "TclLoraFluxGenDatasets":TclLoraFluxGenDatasets,
    "TclLoraFluxTraining":TclLoraFluxTraining,
    "TclLoraCheckpoints":TclLoraCheckPoints
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "TclLoraSaveImages": "TCL Lora Save Images",
    "TclLoraGenDatasets":"TCL Lora Gen Datasets",
    "TclLoraTraining":"TCL Lora Training",
    "TclLoraCheckpoints":"TCL Lora Checkpoints",
    "TclLoraFluxGenDatasets":"TCL Lora Flux Gen Datasets",
    "TclLoraFluxTraining":"TCL Lora Flux Training"
}
