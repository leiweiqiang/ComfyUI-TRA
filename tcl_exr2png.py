import os
import numpy as np
import folder_paths
import skimage.exposure
import OpenImageIO as oiio
from OpenImageIO import ImageInput, ImageOutput
from OpenImageIO import ImageBuf, ImageSpec, ImageBufAlgo

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"

import cv2

HUE = 45
SATURATION = 80
VALUE = 20

ACEScg_to_sRGB_matrix = np.array([
    [1.64102338, -0.32480329, -0.23642469],
    [-0.66366286,  1.61533159,  0.01675635],
    [0.01172189, -0.00828444,  0.98839458]
])

class TclExr2png:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            'required': {
                "filename": ("STRING", {"multiline": False, "default": ""}),
                "subfolder": ("STRING", {"multiline": False, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING","STRING",)
    RETURN_NAMES = ("output","png_output",)    
    FUNCTION = "process"
    CATEGORY = "TCL Research America"

    def process(self, filename, subfolder):
        return greenscreen_removal(filename, subfolder)

def greenscreen_removal(filename, subfolder):

    sigma = 5  # Value for GaussianBlur threshold image

    # in_range and out_range, are used to stretch or shrink the intensity range of the input image
    in_range = (127.5, 255)
    out_range = (0, 255)

    output_directory = folder_paths.get_output_directory()
    # Create output directory if it doesn't exist
    if not os.path.exists(os.path.join(output_directory, f"png_{subfolder}")):
        os.makedirs(os.path.join(output_directory, f"png_{subfolder}"))

    if not os.path.exists(os.path.join(output_directory, f"greenscreen_{subfolder}")):
        os.makedirs(os.path.join(output_directory, f"greenscreen_{subfolder}"))

    # Iterate through the files
    png_filename = convert_exr_to_png(filename, output_directory, subfolder)

    # Load the .exr image in UNCHANGED mode (this will keep the float32 format)
    img = cv2.imread(png_filename, cv2.IMREAD_UNCHANGED)

    # Convert the image from BGR to RGB if it has 3 channels
    if img.shape[2] == 3:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        img_rgb = img

    # Convert to LAB
    lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)

    # Extract A channel
    A = lab[:, :, 1]

    # Threshold A channel
    thresh = cv2.threshold(A, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Blur threshold image
    blur = cv2.GaussianBlur(thresh, (0, 0), sigmaX=sigma, sigmaY=sigma, borderType=cv2.BORDER_DEFAULT)

    # Stretch so that 255 -> 255 and 127.5 -> 0
    mask = skimage.exposure.rescale_intensity(blur, in_range=in_range, out_range=out_range).astype(np.uint8)

    # Fill holes in the mask
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))

    # Add mask to image as alpha channel
    result = img_rgb.copy()
    result = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGRA)
    result[:, :, 3] = mask

    # Save the result in PNG format
    output_file = os.path.join(output_directory, f"png_{subfolder}", f"{os.path.splitext(filename)[0]}.png")
    cv2.imwrite(output_file, result)  # Save as PNG

    return [{
        "filename":os.path.basename(png_filename),
        "subfolder": f"png_{subfolder}",
        "type":"output"
    }, {
        "filename":os.path.basename(output_file),
        "subfolder": f"greenscreen_{subfolder}",
        "type":"output"
    }, ]

# Function to apply the color conversion manually from ACEScg to sRGB
def convert_ACEScg_to_sRGB(image):
    # Apply the linear transformation using the matrix
    sRGB_linear = np.dot(image, ACEScg_to_sRGB_matrix.T)
    # Clamp values to the range [0, 1] to avoid negative values
    sRGB_linear = np.clip(sRGB_linear, 0.0, 1.0)
    # Apply gamma correction to convert linear sRGB to standard sRGB
    sRGB_image = np.where(sRGB_linear <= 0.0031308, 
                          12.92 * sRGB_linear, 
                          1.055 * np.power(sRGB_linear, 1.0 / 2.4) - 0.055)
    return sRGB_image

def get_files(directory_name, file_extension):
    files = os.listdir(directory_name)
    files = [f for f in files if f.endswith(file_extension)]
    files = sorted(files)

    return files

def convert_exr_to_png(filename, output_directory, subfolder):
    source_image = ImageBuf(os.path.join(folder_paths.get_input_directory(), filename))
    # Apply color transformation
    destination_image = ImageBufAlgo.colorconvert(source_image, "acescg","sRGB", True)
    destination_image.set_write_format(oiio.UINT8)
    png_filename = os.path.join(output_directory, f"greenscreen_{subfolder}", f"{os.path.splitext(filename)[0]}.png")
    destination_image.write(png_filename)
    return png_filename

