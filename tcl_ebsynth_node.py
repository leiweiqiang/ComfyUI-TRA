import os
from .utils import get_temp_dir
from torchvision.utils import save_image
import json
import subprocess

class TclEbSynth:

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "keyframe": ("IMAGE",),
                "video_frame_folder": ("PATH",),
                "key_frame_id": ("INT", {"default": 0, "min": 0, "step": 1}),
                "gpu": (["enable", "disable"],)
            },
        }

    RETURN_TYPES = ("PATH",)
    RETURN_NAMES = ("frame_folder",)

    FUNCTION = "ebsynth"

    #OUTPUT_NODE = False

    CATEGORY = "TCL Research America"

    def ebsynth(self, keyframe, video_frame_folder, key_frame_id, gpu):
        is_gpu_on = (gpu == 'enable')
        
        # Create temp output dir
        temp_dir = get_temp_dir()

        # Save keyframe image
        if len(keyframe.shape) == 4:
            assert keyframe.shape[0] == 1
            keyframe = keyframe[0,...]
        keyframe = keyframe.permute(2, 0, 1)
        key_frame_path = os.path.join(temp_dir, 'keyframe.png')
        save_image(keyframe, key_frame_path)

        # Create temp output dir for processed frames
        out_frame_dir = os.path.join(temp_dir, 'output_frames')
        os.makedirs(out_frame_dir)

        # Run the ebsynth on terminal
        execute_ebsynth(key_frame_path, key_frame_id, video_frame_folder, out_frame_dir, is_gpu_on=is_gpu_on)

        return (out_frame_dir,)



def execute_ebsynth(key_frame_path, key_frame_id, in_frame_dir, out_frame_dir, is_gpu_on=False):
    # Get LICENSE SERVER IP
    curdir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(curdir, 'config.json'), 'r') as jfile:
        conf = json.load(jfile)
    os.environ['EBSYNTH_LICENSE_SERVER'] = conf['EBSYNTH_LICENSE_SERVER']

    # Frame count
    nframes = len(os.listdir(in_frame_dir))

    # Prepare the command
    command = [os.path.join(curdir, 'bin', 'ebsynthcmd'), key_frame_path, 
                os.path.join(in_frame_dir, '[####].jpg'), 
                "0", str(key_frame_id), str(nframes-1), 
                os.path.join(out_frame_dir, '[####].jpg')]
    if is_gpu_on: command += ['-usegpu', 'on']
    result = subprocess.run(command, check=True, capture_output=True, text=True)
