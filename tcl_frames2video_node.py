import os
from glob import glob
import folder_paths

import torch
import torchvision
from moviepy.editor import ImageSequenceClip


class TclFrames2Video:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "frame_folder": ("PATH",)
            },
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("video",)
    #OUTPUT_IS_LIST = (True,)

    FUNCTION = "combine_frames"
    CATEGORY = "TCL Research America"

    def combine_frames(self, frame_folder):
        frame_list = sorted(glob(os.path.join(frame_folder, '*.*')))

        vid = []
        for fpath in frame_list:
            f = torchvision.io.read_image(fpath).permute(1,2,0)
            vid.append(f[None, ...])

        vid = torch.concatenate(vid).type(torch.float32) / 255.0
        return (vid, )



class TclSaveVideoFromFrames:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "frame_folder": ("PATH",),
                "video_info": ("VHS_VIDEOINFO", ),
                "filename": ("STRING", {"multiline": False, "default": "ebsynth_output.mp4"})
            },
            "optional": {
                "audio": ("VHS_AUDIO",)
            }
        }
    
    RETURN_TYPES = ()
    #RETURN_NAMES = ("video",)
    #OUTPUT_IS_LIST = (True,)
    OUTPUT_NODE = True
    FUNCTION = "combine_frames_and_save"
    CATEGORY = "TCL Research America"

    def combine_frames_and_save(self, frame_folder, video_info, filename, audio):
        assert 'source_fps' in video_info
        fps = video_info['source_fps']
        # Convert frames to video
        frame_list = sorted(glob(os.path.join(frame_folder, '*.*')))
        clip = ImageSequenceClip(frame_list, fps=fps)

        # Set audio if available
        if audio is not None:
            clip.set_audio(audio)
        
        # Save the video file
        out_dir = folder_paths.get_output_directory()
        if not os.path.exists(out_dir): os.makedirs(out_dir)
        out_vid_path = os.path.join(out_dir, filename)
        clip.write_videofile(out_vid_path, verbose=False, logger=None)

        return {}