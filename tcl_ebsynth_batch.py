import os
import shutil
from pathlib import Path
from .utils import get_temp_dir
from torchvision.utils import save_image
import json
import subprocess
from glob import glob
import torch
import torchvision
from moviepy.editor import ImageSequenceClip


class TclEbSynthBatch:

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "keyframes": ("IMAGE",),
                "video_frame_folder": ("PATH",),
                "video_info": ("VHS_VIDEOINFO", ),
                "filename": ("STRING", {"multiline": False, "default": "ebsynth_output.mp4"}),
                "gpu": (["enable", "disable"],)
            },
            "optional": {
                "audio": ("AUDIO",)
            }
        }

    RETURN_TYPES = ("PATH",)
    RETURN_NAMES = ("video_path",)

    FUNCTION = "ebsynth"

    #OUTPUT_NODE = False

    CATEGORY = "TCL Research America"

    def ebsynth(self, keyframes, video_frame_folder, video_info, filename, gpu, audio):
        is_gpu_on = (gpu == 'enable')

        path_parts = os.path.normpath(video_frame_folder).split(os.sep)
        uuid_str = path_parts[-2]
        
        # Create temp output dir
        temp_dir = get_temp_dir()
        temp_dir = os.path.join(temp_dir, uuid_str)

        # Create keys directory
        keys_dir = os.path.join(temp_dir, 'keys')
        if os.path.exists(keys_dir): shutil.rmtree(keys_dir)
        os.makedirs(keys_dir)

        # Create temp output dir for processed frames
        out_frame_dir = os.path.join(temp_dir, 'output_frames')
        if os.path.exists(out_frame_dir): shutil.rmtree(out_frame_dir)
        os.makedirs(out_frame_dir)

        # keyframe_names = [os.path.basename(filepath) for filepath in filenames]


        # Process each keyframe
        for index, keyframe in enumerate(keyframes):
            # Save keyframe image
            if len(keyframe.shape) == 4:
                assert keyframe.shape[0] == 1
                keyframe = keyframe[0, ...]
            
            # Permute keyframe to (C, H, W)
            keyframe = keyframe.permute(2, 0, 1)

            # Resize keyframe if its size is different than the frame size
            aframe_path = glob(os.path.join(video_frame_folder, '*.*'))[0]
            aframe = torchvision.io.read_image(aframe_path)
            if aframe.shape != keyframe.shape:
                output_size = aframe.shape[1:]
                keyframe = torch.nn.functional.interpolate(keyframe[None,...], size=output_size)[0,...]

            # Extract base name and extension, and format to four digits
            formatted_name = f"{int(index*10):04d}.jpg"

            key_frame_folder = os.path.join(keys_dir, formatted_name)
            save_image(keyframe, key_frame_folder)

        # Run the ebsynth on terminal for each keyframe
        execute_ebsynth(keys_dir, video_frame_folder, out_frame_dir, is_gpu_on=is_gpu_on)

        # Delete keys directory after processing, I'm not sure if this is necessary
        # shutil.rmtree(keys_dir)
        # shutil.rmtree(video_frame_folder)

        assert 'source_fps' in video_info
        fps = video_info['source_fps']
        # Convert frames to video
        frame_list = sorted(glob(os.path.join(out_frame_dir, '*.*')))
        clip = ImageSequenceClip(frame_list, fps=fps)

        # Set audio if available
        if audio is not None:
            clip.set_audio(audio)
        
        # Save the video file
        # out_dir = folder_paths.get_input_directory()
        out_dir = Path('/mnt/sharedfolder/ebsynth_output')
        if not os.path.exists(out_dir): os.makedirs(out_dir)
        out_vid_path = os.path.join(out_dir, filename)
        clip.write_videofile(out_vid_path, verbose=False, logger=None)

        return (out_vid_path,)


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
                '0', '0', str(nframes-1), 
                os.path.join(out_frame_dir, '[####].jpg')]
    command += ['-synthdetail', 'high']
    command += ['-mapping', '15.0']
    command += ['-diversity', '1500.0']
    command += ['-deflicker', '2.5']
    if is_gpu_on: command += ['-usegpu', 'on']
    result = subprocess.run(command, check=True, capture_output=True, text=True)

