import os
import shutil
import uuid
import folder_paths
from glob import glob
import itertools
from .utils import get_temp_dir

from moviepy.editor import VideoFileClip
import torchvision

VIDEO_EXTENSIONS = ['webm', 'mp4', 'mkv', 'gif']


class TclExtractFramesFromVideoFile:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [glob(os.path.join(input_dir, '**', f'*.{ext}'), recursive=True) for ext in VIDEO_EXTENSIONS]
        files = sorted(list(itertools.chain.from_iterable(files)))
        files = [f[len(input_dir)+1:] for f in files]
        return {
            "required": {
                "video": (files,),
            },
        }
    
    RETURN_TYPES = ("PATH", "VHS_VIDEOINFO", "VHS_AUDIO")
    RETURN_NAMES = ("frame_folder", "video_info", "audio")
    
    FUNCTION = "extract_frame_and_save"
    #OUTPUT_NODE = False
    CATEGORY = "TCL Research America"

    def extract_frame_and_save(self, video):
        video_path = os.path.join(folder_paths.get_input_directory(), video)

        # Create temporary output frame directories
        output_dir = get_temp_dir()
        in_frame_dir = os.path.join(output_dir, 'in_frames')
        os.makedirs(in_frame_dir)

        # Extract frames from the input video
        clip = VideoFileClip(video_path)
        for fid, t in enumerate(range_frame_ticks(clip.duration, clip.fps)):
            frame_filename = os.path.join(in_frame_dir, f"{fid:04d}.jpg")
            clip.save_frame(frame_filename, t)

        video_info = {
            'source_fps': clip.fps
        }

        return (in_frame_dir, video_info, clip.audio)


class TclExtractFramesFromVideo:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "video": ("IMAGE",),
            },
        }
    
    RETURN_TYPES = ("PATH", )
    RETURN_NAMES = ("frame_folder", )
    
    FUNCTION = "extract_frame_and_save"
    #OUTPUT_NODE = False
    CATEGORY = "TCL Research America"

    def extract_frame_and_save(self, video):
        # Create temporary output frame directories
        uuid_str = str(uuid.uuid4())
        output_dir = get_temp_dir()
        output_dir = os.path.join(output_dir, uuid_str)
        os.makedirs(output_dir)
        in_frame_dir = os.path.join(output_dir, 'in_frames')
        os.makedirs(in_frame_dir)

        # Save frames
        for fid in range(video.shape[0]):
            frame = video[fid,...].permute(2, 0, 1)
            frame_filename = os.path.join(in_frame_dir, f"{fid:04d}.jpg")
            torchvision.utils.save_image(frame, frame_filename)
            
        return (in_frame_dir, )



# It yields time point for each frame
def range_frame_ticks(duration, fps):
    frame_duration = 1.0 / fps
    t = 0
    while t < duration:
        yield t
        t += frame_duration