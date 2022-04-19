import os

import numpy as np
from PIL import Image
from scipy.ndimage import filters
from scipy.misc import imresize
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def normalize(img):
    ''' Function to normalize an input array to 0-1 '''
    img_min = img.min()
    img_max = img.max()
    return (img - img_min) / (img_max - img_min)

images1 = ['dog.bmp', 'motorcycle.bmp', 'marilyn.bmp', 'bird.bmp',
           'fish.bmp', 'Afghan_girl_before.jpg', 'makeup_before.jpg']

images2 = ['cat.bmp', 'bicycle.bmp', 'einstein.bmp', 'plane.bmp',
           'submarine.bmp', 'Afghan_girl_after.jpg', 'makeup_after.jpg']

freqs = [7, 7, 3, 3, 3, 3, 5]
main_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for i in range(0, len(images1)):
    image1 = mpimg.imread(main_path + '/task1and2_hybrid_pyramid/' + images1[i])/255
    image2 = mpimg.imread(main_path + '/task1and2_hybrid_pyramid/' + images2[i])/255

    if image1.shape[0] + image1.shape[1] < image2.shape[0] + image2.shape[1]:
        image1 = imresize(image1, (image2.shape[0], image2.shape[1]))/255
    if image1.shape[0] + image1.shape[1] > image2.shape[0] + image2.shape[1]:
        image2 = imresize(image2, (image1.shape[0], image1.shape[1]))/255

    freq = freqs[i]
    image1_low = filters.gaussian_filter(image1, sigma=(freq, freq, 0))
    image2_low = filters.gaussian_filter(image2, sigma=(freq, freq, 0))
    image2_high = normalize(image2 - image2_low + 0.5)

    hybrid = normalize(image1_low + image2_high)

    plt.imshow(hybrid)
    plt.waitforbuttonpress()
    plt.imsave('output' + str(i) + '.jpg', hybrid)