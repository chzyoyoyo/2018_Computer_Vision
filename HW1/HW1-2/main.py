import os
from skimage import transform
import matplotlib.image as mpimg
import cv2

# METHOD #2: Resizing + Gaussian smoothing.
images1 = ['dog.bmp', 'motorcycle.bmp', 'marilyn.bmp', 'bird.bmp',
           'fish.bmp', 'Afghan_girl_before.jpg', 'makeup_before.jpg', 'IMG_4647.JPG']
main_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for i in range(0, len(images1)):
    image = cv2.imread(main_path + '/task1and2_hybrid_pyramid/' + images1[i])
    cv2.imwrite('a.jpg', image)
    for (j, resized) in enumerate(transform.pyramid_gaussian(image, downscale=2)):
        # if the image is too small, break from the loop
        if resized.shape[0] < 30 or resized.shape[1] < 30:
            break

        resized = resized * 255
        cv2.imwrite('output{}-{}.jpg'.format(i, j), resized)