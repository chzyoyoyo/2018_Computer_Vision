## Introduction

Structure from Motion (SfM) is an image technique for estimating three-dimensional structures from two-dimensional image sequences that may be grouped together, recovering 3D structure from the projected 2D motion field of a moving object or scene.

The goal of this assignment is to implement SfM from two input images. First, use SIFT to match the keypoints from input images, and use RANSAC to get the best matching points. Use the matching points to get the fundamental matrix and essential matrix, and transform an image to overlay it on the other image. Then, using triangulation to rebuild the 3D model, and map the texture to the mesh of the 3D structure. Finally, we can get a 3D structure from the original 2D images.

<div align=center>
<img src="https://i.imgur.com/KrT8HZ7.jpg" width=70%>
</div>

## SIFT Feature Matching

### Implementation procedure

The goal for this part is to compare two sets of SIFT descriptors from two different images and finding their matching keypoints.

Find the Euclidean distance between all the descriptor in descriptor1 and descriptor2. And each descriptor in descriptor1 will calculate lots of Euclidean distance with all descriptors in descriptor2. Then we find the Min and second Min Euclidean distance for each descriptor in descriptor1.

If the Min is less than threshold (second Min Euclidean distance), we store index of descriptor in descriptor1 and descriptors in descriptor2 which calculating Min Euclidean distance in the 'Match'

### Experimental results

<div align=center>
<img src="https://i.imgur.com/ZrKAh6n.jpg" width=80%>
</div>

## Fundamental Matrix

### Implementation procedure

To figure out the relationship between two images, we have to find the corresponding points. By SIFT algorithm, we can easily get the corresponding points. Then we use RANSAC to try other samples many times, which can ensure that having the best inliers. After finishing feature detection and point matching, we estimate fundamental matrix using feature pairs in two images.

The fundamental matrix F is defined by ![](http://latex.codecogs.com/gif.latex?x'^TFx=0).
If x = [u  v  1]T and x' = [u'  v'  1]T, we will get the following formula. By 8-point algorithm, calculate least squares solution using SVD on equations from 8 pairs of correspondences. Finally, we get the fundamental matrix of two images. Fundamental matrix maps from a point in one image to a line in the other image, which is the epipolar line.

<div align=center>
<img src="https://i.imgur.com/mIjRMIF.jpg" width=60%>
</div>

### Experimental results

![](https://i.imgur.com/lJxNxJ6.png)

## Essential Matrix

### Implementation procedure

First, we use ![](http://latex.codecogs.com/gif.latex?E=K'^TFK) to evaluate the initial essential matrix. K is the intrinsic matrix of the two cameras.  F is the fundamental matrix that we have gotten. Then we use SVD twice. The first time we use SVD to get the initial U, D, V matrix. In order to satisfy the rank deficiency, we set ![](http://latex.codecogs.com/gif.latex?D_{33}) to be 0. After we use the new D to get our new essential matrix ![](http://latex.codecogs.com/gif.latex?(E=U*D*V'))![](http://latex.codecogs.com/gif.latex?(V'=V^T)), we do the SVD again and obtain the final U and V matrix. Next, we set two matrix

<div align=center>
<img src="https://i.imgur.com/D2bmSwc.jpg" width=50%>
</div>

With these two matrix, we are able to estimate the R matrix (rotation matrix).

![](http://latex.codecogs.com/gif.latex?R'=UW^TV^T)

![](http://latex.codecogs.com/gif.latex?R'=UWV^T)

Use ![](http://latex.codecogs.com/gif.latex?det(R)) to decide it is mirror matrix or not. If ![](http://latex.codecogs.com/gif.latex?det(R)) < 0, use R = -R to make it correct.
Next we use ![](http://latex.codecogs.com/gif.latex?T=U*Z*U') ![](http://latex.codecogs.com/gif.latex?(U'=U^T)) to get first t, the second t is T2 = -T. 
Now we get four (R, t), each R and t has two solutions, but there is only one (R, t) is the correct answer.
So we use triangulation to determine which (R, t) is correct.
For example,

![](https://i.imgur.com/RdtX9vM.png)

After the triangulation, we obtain four result, each one of them represent one (R, t).
In this case, only the points of the second result are in front of the camera. 
Finally, we know which (R, t) is the correct solution.


## Triangulation

### Implementation procedure

To get the final 3D points from 2d image. we have to first project the 2d point into a 3d ray, and find the intersection between two rays. But sometimes these two rays are skew due to the error in image resolution or feature extracting. In these situation we have to find the nearest point between the rays.

To find the correct 3D points, we use linear triangulation, and minimizing the algebraic error with SVD. This algorithm uses the two equations for perspective projection to solve for the 3D point that are optimal in a least squares sense. Each perspective camera model gives rise to two equations on the three entries of ![](http://latex.codecogs.com/gif.latex?X_i)，Combining these equations we get an over determined homogeneous system of linear equations that we can solve with SVD。

<div align=center>
<img src="https://i.imgur.com/WGceWTY.jpg" width=60%>
</div>

### Experimental results

![](https://i.imgur.com/Zw1hKpy.png)

## Final Results

<div align=center>
<img src="https://i.imgur.com/itEygIr.jpg" width=70%>
<img src="https://i.imgur.com/07VQFiT.jpg" width=70%>
</div>

## Work assignment plan between team members:

0416025 呂翊愷: Fundamental Matrix  
0416061 陳則佑: Essential Matrix  
0416081 趙賀笙: Triangulation, SIFT Feature Matching  