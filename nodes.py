from .tcl_exr2png import TclExr2png
from .tcl_relighting import TclRelighting
from .tcl_relighting_api import TclRelightingApi
from .tcl_relighting_zip import TclRelightingZip
from .tcl_folder2zip import TclFolder2Zip

NODE_CLASS_MAPPINGS = {
    "TclExr2png":TclExr2png,
    "TclRelighting":TclRelighting,
    "TclFolder2Zip":TclFolder2Zip,
    "TclRelightingApi":TclRelightingApi,
    "TclRelightingZip":TclRelightingZip
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "TclExr2png":"Tcl Exr2png",
    "TclRelighting":"Tcl Relighting",
    "TclFolder2Zip":"Tcl Folder2Zip",
    "TclRelightingApi":"Tcl Relighting Api",
    "TclRelightingZip":"Tcl Relighting Zip"
}
