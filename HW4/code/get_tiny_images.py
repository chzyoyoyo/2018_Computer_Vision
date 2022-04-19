from PIL import Image

import pdb
import numpy as np

def get_tiny_images(image_paths):

    tiny_images = []
    for img_path in image_paths:
        img = Image.open(img_path)
        img_resized = np.asarray(img.resize((16, 16), Image.ANTIALIAS)).reshape(1,-1)
        tiny_images.extend(img_resized)
    tiny_images = np.asarray(tiny_images)

    return tiny_images
