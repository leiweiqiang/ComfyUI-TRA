from .tcl_exr2png import TclExr2png
from .tcl_relighting import TclRelighting

NODE_CLASS_MAPPINGS = {
    "TclExr2png":TclExr2png,
    "TclRelighting":TclRelighting
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "TclExr2png":"Tcl Exr2png",
    "TclRelighting":"Tcl Relighting"
}
