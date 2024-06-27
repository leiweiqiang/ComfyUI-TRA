from .tcl_ebsynth_node import TclEbSynth
from .tcl_extract_video_frames_node import TclExtractFramesFromVideoFile, TclExtractFramesFromVideo
from .tcl_frames2video_node import TclFrames2Video, TclSaveVideoFromFrames


NODE_CLASS_MAPPINGS = {
    "TclEbSynth": TclEbSynth,
    "TclExtractFramesFromVideoFile": TclExtractFramesFromVideoFile,
    "TclExtractFramesFromVideo": TclExtractFramesFromVideo,
    "TclFrames2Video": TclFrames2Video,
    "TclSaveVideoFromFrames": TclSaveVideoFromFrames
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "TclEbSynth": "TCL EbSynth",
    "TclExtractFramesFromVideoFile": "TCL Extract Frames (From File)",
    "TclExtractFramesFromVideo": "TCL Extract Frames (From Video)",
    "TclFrames2Video": "TCL Combine Frames",
    "TclSaveVideoFromFrames": "TCL Save Video (From Frames)"
}
