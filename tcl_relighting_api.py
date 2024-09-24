import uuid
from .greenscreen_utils import greenscreen_removal
import logging
import json
import os
import shutil


def process_path(input_path):
    new_uuid = str(uuid.uuid4())
    new_symlink_path = f"/ComfyUI/input/{new_uuid}"
    if not os.path.exists(new_symlink_path):
        os.symlink(os.path.join("/relighting_inputs", input_path), new_symlink_path)

    slapcomp_path = os.path.join(new_symlink_path, 'slapcomp')
    relighting_path = os.path.join(new_symlink_path, 'relighting')

    if os.path.exists(slapcomp_path):
        shutil.rmtree(slapcomp_path)

    if os.path.exists(relighting_path):
        shutil.rmtree(relighting_path)

    file_list = os.listdir(new_symlink_path)
    files_in_dir = [
        {"filename": file, "subfolder": new_uuid, "type": "input"}
        for file in file_list
        if os.path.isfile(os.path.join(new_symlink_path, file))
    ]
    for index, keyframe in enumerate(files_in_dir):
        result = greenscreen_removal(keyframe["filename"], new_uuid)

    return f"./output/png_{new_uuid}",f"./input/{new_uuid}/results_slapcomp",f"./input/{new_uuid}/results_slapcomp/{{:04d}}.png",f"./input/{new_uuid}/results_relighting",f"./input/{new_uuid}/results_relighting/{{:04d}}.png",0,len(file_list),


class TclRelightingApi:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            'required': {
                "keyframes": ("STRING", {"multiline": False, "default": ""}),
                "input_path": ("STRING", {"multiline": False, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING","STRING","STRING","STRING","STRING","INT","INT",)
    RETURN_NAMES = ("png_dir","slapcomp_dir","slapcomp_pattern","relighting_dir","relighting_pattern","start_index","image_load_cap",)    
    FUNCTION = "process"
    CATEGORY = "TCL Research America"


    def process(self, keyframes, input_path):
        if len(input_path) > 0:
            return process_path(input_path)
        else:     
            subfolder = str(uuid.uuid4())
            output = []
            json_object = json.loads(keyframes)
            for index, keyframe in enumerate(json_object):
                result = greenscreen_removal(keyframe["filename"], subfolder)
                logging.info(result)
                output.append(result)

            return f"./output/png_{subfolder}",f"./output/slapcomp_{subfolder}",f"./output/slapcomp_{subfolder}/{{:04d}}.png",f"./output/relighting_{subfolder}",f"./output/relighting_{subfolder}/{{:04d}}.png",0,len(keyframes),
