import numpy as np
import skimage as sk
import skimage.io as skio
import skimage.transform as sktr
import scipy.misc as scm
import sys
from scipy.signal import convolve2d as c2d

#image cropping
def cropImage(img):
  height, width = img.shape
  cropHeight = int(height*0.1)
  cropWidth = int(width*0.1)
  return img[cropHeight:img.shape[0]-cropHeight, cropWidth:img.shape[1]-cropWidth]


def detectEdge(img):
  sobelX = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
  sobelY = sobelX.T

  img = c2d(img, sobelX)
  img = c2d(img, sobelY)
  return img

def pyramid(imname):
  # read in the image
  im = skio.imread(imname)

  # convert to double (might want to do this later on to save memory)    
  im = sk.img_as_float(im)
      
  # compute the height of each part (just 1/3 of total)
  height = int(np.floor(im.shape[0] / 3.0))
  print('height: ', height)

  # separate color channels
  b = im[:height]
  g = im[height: 2*height]
  r = im[2*height: 3*height]

  original_b, original_r, original_g = b, r, g
  b = cropImage(b)
  g = cropImage(g)
  r = cropImage(r)



  # im_out = np.dstack([r, g, b])
  # fname = 'unaligned_' + imname
  # scm.imsave(fname, im_out)
  # skio.imshow(im_out)
  # skio.show()

  # Apply edge detection
  b = detectEdge(b)
  g = detectEdge(g)
  r = detectEdge(r)

  #helper functions
  def get_similar(r, g, b, rad): 
    bg_similar = similarity(b, g, rad)
    br_similar = similarity(b, r, rad)
    return (bg_similar, br_similar)


  #naive 15-pixel implementation
  def similarity(img_b, img, rad):
      mat = np.zeros((rad*2, rad*2))
      for i in range(-rad, rad):
          for j in range(-rad, rad):
                  img_new = np.roll(img, i, axis=0)
                  img_new = np.roll(img_new, j, axis=1)
                  ssd_val = ssd(img_b, img_new)
                  mat[i+rad, j+rad] = ssd_val

      lowest = mat.argmin() 
      row_shift = (lowest // (rad*2)) - rad ##check this part **
      col_shift = (lowest % (rad*2)) - rad ##check this part **
      return (row_shift, col_shift)


  def ssd(img_1, img_2):
    ssd = np.sum((img_1 - img_2) **2)
    return ssd


  #pyramid implementation 
  f = 20
  rad = int((height // f) // 5) 
  total_row_shift_g, total_col_shift_g, total_row_shift_r, total_col_shift_r = 0, 0, 0, 0


  while (f>=1): 
    #downscale first
    # print('rad, f: ', rad, ', ',f)
    mini_b = sktr.downscale_local_mean(b, (f, f))
    mini_r = sktr.downscale_local_mean(r, (f, f))
    mini_g = sktr.downscale_local_mean(g, (f, f))
    # print('image size: ', mini_b.shape)

    #compute similarity
    similar_result = get_similar(mini_r, mini_g, mini_b, rad)
    bg_result = similar_result[0] #x, y shift for g
    br_result = similar_result[1] #x, y shift for r 

    #rolling
    total_row_shift_g += (bg_result[0] * f) 
    total_col_shift_g += (bg_result[1] * f) 
    total_row_shift_r += (br_result[0] * f) 
    total_col_shift_r += (br_result[1] * f) 

    g = np.roll(g, bg_result[0] * f, axis=0)
    g = np.roll(g, bg_result[1] * f, axis=1)

    r = np.roll(r, br_result[0] * f, axis=0)
    r = np.roll(r, br_result[1] * f, axis=1)

    #updating factors
    f = int(f / 2)
    rad = int(rad / 2)


  # create a color image
  print('total_row_shift_g, total_col_shift_g: ', total_row_shift_g, ', ', total_col_shift_g)
  print('total_row_shift_r, total_col_shift_r: ', total_row_shift_r, ', ', total_col_shift_r)
  original_g = np.roll(original_g, total_row_shift_g, axis=0)
  original_g = np.roll(original_g, total_col_shift_g, axis=1)
  original_r = np.roll(original_r, total_row_shift_r, axis=0)
  original_r = np.roll(original_r, total_col_shift_r, axis=1)

  im_out = np.dstack([original_r, original_g, original_b])

  # save the image
  fname = 'new_' + imname
  scm.imsave(fname, im_out)

  # display the image
  skio.imshow(im_out)
  skio.show()