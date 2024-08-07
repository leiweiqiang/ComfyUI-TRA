import os
from .utils import get_temp_dir
from torchvision.utils import save_image
import json
import subprocess
from glob import glob
import torch
import torchvision

class TclEbSynth:

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "keyframes": ("IMAGE",),
                "filenames": ("PATH",),
                "video_frame_folder": ("PATH",),
                "gpu": (["enable", "disable"],)
            },
        }

    RETURN_TYPES = ("PATH",)
    RETURN_NAMES = ("frame_folder",)

    FUNCTION = "ebsynth"

    #OUTPUT_NODE = False

    CATEGORY = "TCL Research America"

    def ebsynth(self, keyframes, filenames, video_frame_folder, gpu):
        is_gpu_on = (gpu == 'enable')

        print(filenames)
        
        # Create temp output dir
        temp_dir = get_temp_dir()

        # Create keys directory
        keys_dir = os.path.join(temp_dir, 'keys')
        os.makedirs(keys_dir, exist_ok=True)

        # Create temp output dir for processed frames
        out_frame_dir = os.path.join(temp_dir, 'output_frames')
        os.makedirs(out_frame_dir, exist_ok=True)

        keyframe_names = [os.path.basename(filepath) for filepath in filenames]


        # Process each keyframe
        for index, keyframe in enumerate(keyframes):
            # Save keyframe image
            if len(keyframe.shape) == 4:
                assert keyframe.shape[0] == 1
                keyframe = keyframe[0, ...]
            
            # Permute keyframe to (C, H, W)
            keyframe = keyframe.permute(2, 0, 1)

            # Extract base name and extension, and format to four digits
            base_name, ext = os.path.splitext(keyframe_names[index])
            formatted_name = f"{int(base_name):04d}{ext}"

            key_frame_folder = os.path.join(keys_dir, formatted_name)
            save_image(keyframe, key_frame_folder)

        # Run the ebsynth on terminal for each keyframe
        execute_ebsynth(keys_dir, video_frame_folder, out_frame_dir, is_gpu_on=is_gpu_on)

        # Delete keys directory after processing, I'm not sure if this is necessary
        # shutil.rmtree(keys_dir)

        return (out_frame_dir,)


def execute_ebsynth(key_frame_dir, in_frame_dir, out_frame_dir, is_gpu_on=False):
    # Get LICENSE SERVER IP
    curdir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(curdir, 'config.json'), 'r') as jfile:
        conf = json.load(jfile)
    os.environ['EBSYNTH_LICENSE_SERVER'] = conf['EBSYNTH_LICENSE_SERVER']

    # Frame count
    nframes = len(os.listdir(in_frame_dir))

    # Extract key_frame_id from the first file in key_frame_dir
    # first_file_name = sorted(os.listdir(key_frame_dir))[0]
    # key_frame_id = os.path.splitext(first_file_name)[0]
    # key_frame_id = str(int(key_frame_id))

    # Prepare the command
    command = [os.path.join(curdir, 'bin', 'ebsynthcmd'), 
               os.path.join(key_frame_dir, '[####].jpg'), 
                os.path.join(in_frame_dir, '[####].jpg'), 
                "0", str(nframes-1), str(nframes-1), 
                os.path.join(out_frame_dir, '[####].jpg')]
    if is_gpu_on: command += ['-usegpu', 'on']
    result = subprocess.run(command, check=True, capture_output=True, text=True)

