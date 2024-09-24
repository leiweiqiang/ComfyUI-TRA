import os
import numpy as np
import cv2
import skimage.exposure
import folder_paths
import OpenImageIO as oiio
from OpenImageIO import ImageBuf, ImageBufAlgo
import logging

ACEScg_to_sRGB_matrix = np.array([
    [1.64102338, -0.32480329, -0.23642469],
    [-0.66366286,  1.61533159,  0.01675635],
    [0.01172189, -0.00828444,  0.98839458]
])

def greenscreen_removal(filename, subfolder):
    sigma = 5  # Value for GaussianBlur threshold image
    in_range = (127.5, 255)
    out_range = (0, 255)

    output_directory = folder_paths.get_output_directory()
    if not os.path.exists(os.path.join(output_directory, f"png_{subfolder}")):
        os.makedirs(os.path.join(output_directory, f"png_{subfolder}"))

    if not os.path.exists(os.path.join(output_directory, f"greenscreen_{subfolder}")):
        os.makedirs(os.path.join(output_directory, f"greenscreen_{subfolder}"))

    png_filename = convert_exr_to_png(filename, output_directory, subfolder)

    # logging.info(png_filename)

    img = cv2.imread(png_filename, cv2.IMREAD_UNCHANGED)

    if img.shape[2] == 3:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        img_rgb = img

    lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
    A = lab[:, :, 1]

    thresh = cv2.threshold(A, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    blur = cv2.GaussianBlur(thresh, (0, 0), sigmaX=sigma, sigmaY=sigma, borderType=cv2.BORDER_DEFAULT)

    mask = skimage.exposure.rescale_intensity(blur, in_range=in_range, out_range=out_range).astype(np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))

    result = img_rgb.copy()
    result = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGRA)
    result[:, :, 3] = mask

    output_file = os.path.join(output_directory, f"png_{subfolder}", f"{os.path.splitext(filename)[0]}.png")
    cv2.imwrite(output_file, result)

    return {"alpha":{
        "filename":os.path.basename(png_filename),
        "subfolder": f"png_{subfolder}",
        "type":"output"
    }, "greenscreen": {
        "filename":os.path.basename(output_file),
        "subfolder": f"greenscreen_{subfolder}",
        "type":"output"
    }}

def convert_exr_to_png(filename, output_directory, subfolder):
    source_image = ImageBuf(os.path.join(folder_paths.get_input_directory(), filename))
    destination_image = ImageBufAlgo.colorconvert(source_image, "acescg","sRGB", True)
    destination_image.set_write_format(oiio.UINT8)
    png_filename = os.path.join(output_directory, f"greenscreen_{subfolder}", f"{os.path.splitext(filename)[0]}.png")
    destination_image.write(png_filename)
    return png_filename