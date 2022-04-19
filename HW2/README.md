## Introduction
Panoramic stitching is an early success of computer vision. Matthew Brown and David G. Lowe published a famous panoramic image stitching paper in 2007. Since then, automatic panorama stitching technology has been widely adopted in many applications such as Google Street View, panorama photos on smartphones, and stitching software such as Photosynth and AutoStitch.

The goal of this assignment is to detect, extract, and compare the SIFT points in order to match the SIFT keypoints from multiple input images. After we use RANSAC and get the Homography transformation matrix, we can transform an image and overlay it on the top of the other image. Then, using multi band blending to stitch images. Finally, we can get a panorama image.

<div align=center>
<img src="https://i.imgur.com/FUmOiYp.jpg" width=70%>
</div>

## SIFT Feature Matching
### Implementation procedure
The goal for this part is to compare two sets of SIFT descriptors from two different images and finding their matching keypoints.

Find the Euclidean distance between all the descriptor in descriptor1 and descriptor2. And each descriptor in descriptor1 will calculate lots of Euclidean distance with all descriptors in descriptor2. Then we find the Min and second Min Euclidean distance for each descriptor in descriptor1.

If the Min is less than threshold (second Min Euclidean distance), we store index of descriptor in descriptor1 and descriptors in descriptor2 which calculating Min Euclidean distance in the 'Match'

### Experimental results

<div align=center>
<img src="https://i.imgur.com/5o3mMxK.jpg" width=70%>
</div>

## Homography
### Introduction

In order to do the RANSAC, we write a code to figure out the homography matrix for any four points.

### Implementation procedure

<div align=center>
<img src="https://i.imgur.com/IPoTCLz.jpg" width=30%>
</div>

To find the homography matrix, we set <img src="http://chart.googleapis.com/chart?cht=tx&chl= h_{33}=1" style="border:none;"> and use 4 pair of feature points to compute <img src="http://chart.googleapis.com/chart?cht=tx&chl= h_{11}" style="border:none;">~<img src="http://chart.googleapis.com/chart?cht=tx&chl= h_{32}" style="border:none;">.

<div align=center>
<img src="https://i.imgur.com/kGU4EJO.jpg" width=60%>
</div>


First, we find a library named ``sympy``, and there are a function named ``solve``. It is the most simple and powerful way to figure out the answer to any function whether it is linear or not. However, it takes too much time to compute the homography matrix, so we choose another way. ``numpy.linalg.solve()`` is only capable to solve a linear matrix equation, but it is indeed much faster than sympy.

### Experimental results

<div align=center>
<img src="https://i.imgur.com/MnJaSSj.jpg" width=90%>
</div>

## RANSAC

### Implementation procedure

First, we plan to iterate RANSAC 500 times for each pair of pictures. For random sampling, we use a function ``random_partition`` to get 4 random numbers, and take these numbers as the indices of the points in two pictures.  We assume that these points are the inliers of  all the points. Then, by calling function ``findHomography``, which has been mentioned, we get the homography matrix of the two pictures. Using the homography matrix, we can compute the transformed coordinates of the ouliers. The way to compute the error is to calculate the Euclidean Distance between the original coordinates of outliers and the transformed coordinates of outliers. By doing above process 500 times, we can get the least error, which is also the best model.

### Experimental results

<div align=center>
<img src="https://i.imgur.com/wOpTR44.jpg" width=70%>
</div>


## Pyramid Blending
### Implementation procedure

To get the blending version of the joint image, we have to get the Laplacian pyramids of the two pictures. However, there is no exclusive function for that, so we get the Gassian pyramid first by using function ``cv2.pyrDown``, which be able to return the lower level of the original image. A level in Laplacian Pyramid is formed by the difference between that level in Gaussian Pyramid and expanded version of its upper level in Gaussian Pyramid, so we use ``cv2.subtract`` to get the difference, which is the Laplacian pyramid. Then, join the part of one picture and the part of another picture in each levels of Laplacian Pyramids. Finally from this joint image pyramids, reconstruct the original image.

<div align=center>
<img src="https://i.imgur.com/6laW5hB.jpg" width=70%>
</div>

### Experimental results

<div align=center>
<img src="https://i.imgur.com/rj5nI7V.jpg" width=70%>
</div>

<div align=center>
<img src="https://i.imgur.com/THouzLz.jpg" width=70%>
</div>

## Discussion
First, since the way to get Homography matrix is not fast enough, we choose the another way. Then, at the RANSAC part, we take a lot of time to figure out how to compute the error of the model. Besides, we take most time to solve the edge problem. There were always having a black line on the image edge when we did image stitching. At last, we found a function in OpenCV could help us to solving the problem, so finally the result is perfect.

## Conclusion
Although we already use RANSAC to find the most correct homography matrix, sometimes it still has some flaw. We still need to work on it.

## Work assignment plan between team members

0416025 呂翊愷: RANSAC, image blending  
0416061 陳則佑: Homography  
0416081 趙賀笙: SIFT, image blending with mask  

