from .tcl_ebsynth_node import TclEbSynth
from .tcl_ebsynth_batch import TclEbSynthBatch
from .tcl_extract_video_frames_node import TclExtractFramesFromVideoFile, TclExtractFramesFromVideo
from .tcl_frames2video_node import TclFrames2Video, TclSaveVideoFromFrames
from .tcl_yolov8 import TclYoloV8Segmentation
from .tcl_yolov9 import TclYoloV9Segmentation
from .tcl_lora_save_images import TclLoraSaveImages
from .tcl_lora_gen_datasets import TclLoraGenDatasets

NODE_CLASS_MAPPINGS = {
    "TclEbSynth": TclEbSynth,
    "TclEbSynthBatch": TclEbSynthBatch,
    "TclExtractFramesFromVideoFile": TclExtractFramesFromVideoFile,
    "TclExtractFramesFromVideo": TclExtractFramesFromVideo,
    "TclFrames2Video": TclFrames2Video,
    "TclSaveVideoFromFrames": TclSaveVideoFromFrames,
    "TclYoloV8Segmentation": TclYoloV8Segmentation,
    "TclYoloV9Segmentation":TclYoloV9Segmentation,
    "TclLoraSaveImages":TclLoraSaveImages,
    "TclLoraGenDatasets":TclLoraGenDatasets
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "TclEbSynth": "TCL EbSynth",
    "TclEbSynthBatch": "TCL EbSynth (Batch)",
    "TclExtractFramesFromVideoFile": "TCL Extract Frames (From File)",
    "TclExtractFramesFromVideo": "TCL Extract Frames (From Video)",
    "TclFrames2Video": "TCL Combine Frames",
    "TclSaveVideoFromFrames": "TCL Save Video (From Frames)",
    "TclYoloV8Segmentation": "TCL YoloV8 Segmentation",
    "TclYoloV9Segmentation": "TCL YoloV9 Segmentation",
    "TclLoraSaveImages": "TCL Lora Save Images",
    "TclLoraGenDatasets":"TCL Lora Gen Datasets"
}
