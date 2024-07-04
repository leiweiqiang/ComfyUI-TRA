from ultralytics import YOLO
from PIL import Image
import numpy as np
import torch
import os
import folder_paths

# Download yolo v8 files under ComfyUI/model/yolov8
# Model weight links
# https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n-seg.pt
# https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8s-seg.pt
# https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8m-seg.pt
# https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8l-seg.pt
# https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8x-seg.pt

folder_paths.add_model_folder_path('yolov8', os.path.join(folder_paths.models_dir, 'yolov8'))

CLASS_ID2NAME = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}
CLASS_NAME2ID = {v:k for k, v in CLASS_ID2NAME.items()}

class TclYoloV8Segmentation:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            'required': {
                'image': ('IMAGE', ),
                'model_name': (folder_paths.get_filename_list('yolov8'), ),
                'class_name': (list(CLASS_NAME2ID.keys()), )
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image_overlay", 'mask')
    FUNCTION = "segment"
    #OUTPUT_NODE = False
    CATEGORY = "TCL Research America"

    def segment(self, image, model_name, class_name):
         # Load YOLO model weights
        model_path = os.path.join(folder_paths.models_dir, 'yolov8', model_name)
        yolo_model = YOLO(model_path)

        # Convert tensor to PIL image
        image_np = image.cpu().numpy()  # Change from CxHxW to HxWxC for Pillow
        input_image = Image.fromarray((image_np.squeeze(0) * 255).astype(np.uint8))

        # Inference
        results = yolo_model(input_image)

        # Get the results
        masks = results[0].masks.data
        boxes = results[0].boxes.data

        # Select masks
        class_id = CLASS_NAME2ID[class_name]
        pred_cls = boxes[:, 5]
        selected_cls_idx = torch.where(pred_cls == class_id)
        selected_masks = masks[selected_cls_idx]
        mask_merged = torch.any(selected_masks, dim=0).int() * 255

        # Create overlay image
        overlay_img = results[0].plot()  # plot a BGR numpy array of predictions
        overlay_img = Image.fromarray(overlay_img[...,::-1])  # RGB PIL image
        overlay_img = torch.tensor(np.array(overlay_img).astype(np.float32) / 255.0)  # Convert back to CxHxW
        overlay_img = torch.unsqueeze(overlay_img, 0)

        return overlay_img, mask_merged