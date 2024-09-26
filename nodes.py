from .tcl_fresco import TclFresco
from .tcl_fresco_wraped_noise import TclFrescoWrapedNoise

NODE_CLASS_MAPPINGS = {
    "TclFresco": TclFresco,
    "TclFrescoWrapedNoise": TclFrescoWrapedNoise,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "TclFresco": "Tcl Fresco",
    "TclFrescoWrapedNoise": "Tcl Fresco Wraped Noise",
}
