import os
import shutil
import subprocess
import logging

class TclRelightingZip:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                "images": ("IMAGE",),
                "png_dir": ("STRING", {"multiline": False, "default": ""}),
                "slapcomp_dir": ("STRING", {"multiline": False, "default": ""}),
                "relighting_dir": ("STRING", {"multiline": False, "default": ""}),
            },
        }

    RETURN_TYPES = ("JSON",)
    RETURN_NAMES = ("output",)    
    FUNCTION = "process"
    CATEGORY = "TCL Research America"

    def process(self, images, png_dir, slapcomp_dir, relighting_dir):
        # Extract UUID by removing "png_" from png_dir
        uuid = os.path.basename(png_dir).replace("png_", "")

        # Define output file (zip file)
        output_file = os.path.join("./output", f"{uuid}.zip")

        logging.info(output_file)

        # Check if all directories exist
        if not os.path.exists(png_dir):
            return {"error": f"Directory {png_dir} does not exist."}
        if not os.path.exists(slapcomp_dir):
            return {"error": f"Directory {slapcomp_dir} does not exist."}
        if not os.path.exists(relighting_dir):
            return {"error": f"Directory {relighting_dir} does not exist."}

        try:
            # Create the zip file containing the renamed directories
            command = ["zip", "-r", output_file, png_dir, slapcomp_dir, relighting_dir]
            result = subprocess.run(command, check=True, capture_output=True, text=True)

            # Check if the zip command was successful
            if result.returncode != 0:
                return {"error": result.stderr}

            logging.info(f"{uuid}.zip")

            # Return the path of the generated zip file
            return {
                "output": f"https://relighting-comfyui.tcl-research.us/api/nuke/download?filename={uuid}.zip&type=output"
            },

        except subprocess.CalledProcessError as e:
            return {"error": f"Zipping failed: {e.stderr}"}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}