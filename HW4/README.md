## Introduction

The goal of this assignment is to build a classifier to categorize images into one of 15 scene types. Specifically, we will examine the task of scene recognition starting with tiny images and nearest neighbor classification and then move on to the following techniques: bag of SIFT feature detection and linear SVM classifier.

Bag of SIFT feature detection is implemented by bag of words. In other words, first detect SIFT features from all the training images, and use K-means to group the features in K cluster. Finally, the center of the cluster is the feature of the cluster, and build a histogram of the ratio of these features appeared in the test image. Since the different scene has the different ratio of each features, we can differentiate the scene by doing so.

![](https://i.imgur.com/tTICMf2.png)

## Tiny Images Representation

### Implementation procedure

To calculate the distance between the two images, we have to build the tiny images representation,  simply resize all training image and test images to a small, fixed resolution 16*16. As a result, the calculation amount can be decreased and save the execution time effectively.

First, to resize the image, we use ``numpy.resize`` function and then use function np.asarray to vectorize tiny images. By doing the above steps, we can get tiny images to compute the Euclidean distance more conveniently.

## Nearest Neighbor Classifier

### Implementation procedure

The nearest neighbor classifier will predict the category for every test image by finding the training image with most similar features. To implement nearest neighbor classifier, we have to use kNN algorithm, which is abbreviation of K-nearest neighbors algorithm. The training points are separated into several regions to predict the classification of a new test point. Given a training vector, kNN algorithm identifies the nearest k neighbors and assigns the training vector to the most common category among its k nearest neighbors.

To find the nearest neighbor, we use ``scipy.spatial.distance.cdist`` function to calculate the distance between training images and test images, and then we use numpy.argmin to find the minimum distance. Finally, the test image will be classified as the category of the nearest training image.

<div align=center>
<img src="https://i.imgur.com/hF7kqeE.jpg" width=90%>
</div>

## Bag of SIFT Representation

### Implementation procedure

To use this method, we need to use SIFT first. We have already done this for many times in past assignments, so I start from the next step. After we find the features of all the images, we use K-means to group all features. The python function named kmeans is the function that help us to do the K-means cluster. By doing so, we can get many points which represents their cluster. With these points, it prevents our program from wasting too many time. In addition, too many features will create too many dimensions, and this will cause the curse of dimension. Therefore, it is necessary to do bag of SIFT.

![](https://i.imgur.com/9Zfiwq0.png)


After we get those features, how do we use them to define a picture. We calculate the count of those features of all the images. These information of train images create points in the hyperspace whose dimension is decided by the K-means, so we can use nearest neighbor or SVM to classify the test image.

<div align=center>
<img src="https://i.imgur.com/7g8AEpe.jpg" width=80%>
</div>


## Linear SVM Classifier

### Implementation procedure

There are many classifier to do the pattern recognition, SVM is one of them. It is a classifier that separate the classes by an hyperplane. In homework 4, SVM is used to classify the points which represent the train images in the hyperspace. With these hyperplane, when we test a new image, we only need to find its position in the hyperspace and we can estimate what is it. To implement this method, we use python function “svmLinear”, as the figure shown below.


![](https://i.imgur.com/lYa86KE.png)


SVM design the linear classifier as f(x)=sgn(w dot x+b). In the real case, there are many hyperplane that we can find to separate the classes. In SVM, it choose the hyperplane which has the largest margin. 

<div align=center>
<img src="https://i.imgur.com/F4tbX5k.jpg" width=90%>
</div>

## Bonus: Convolutional Neural Network

### Implementation procedure

To achieve the goal of scene recognition, we adapt the architecture from the famous network AlexNet. We setup the NN with python and keras, and train it with the 1500 training image. However, the result wasn’t ideal. After 50 epochs training,  we got around 99% accuracy on training data, but only 40% accuracy on test set, which is caused by the overfitting problem. To solve this problem, we adapt two techniques, data augmentation and transfer learning. 

<div align=center>
<img src="https://i.imgur.com/hwyZvEu.jpg" width=70%>
</div>

### Data Augmentation

Data augmentation is one of the techniques for reducing overfitting. We enlarge our dataset by using horizontal flip and random crop, and generate 10 new images from 1 training data. 

![](https://i.imgur.com/iOhZnIC.png)

### Transfer Learning

Transfer learning is another techniques for reducing overfitting. The general idea of transfer learning is to use knowledge learned from tasks for which a lot of labelled data is available in settings where only little labelled data is available. We took a pre-trained models on GitHub, and continue our training on that model.

### Result

<img src="https://i.imgur.com/6SwVyGZ.jpg" width=80%>
<img src="https://i.imgur.com/2XWoFRY.jpg" width=80%>

## Final Result

<img src="https://i.imgur.com/E1RDLtM.jpg" width=70%>
<img src="https://i.imgur.com/pnpzEfG.jpg" width=70%>
<img src="https://i.imgur.com/m3tyaRp.jpg" width=70%>

## Work assignment plan between team members:

0416025 呂翊愷: Tiny Images Representation, Nearest Neighbor Classifier  
0416061 陳則佑: Bag of SIFT Representation, Linear SVM Classifier  
0416081 趙賀笙: Convolutional Neural Network  

