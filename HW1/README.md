## Task 1: Hybrid Image

### Implementation procedure
- First, obtain the images and check whether the images are the same size. If they have different sizes, resize the smaller one to the bigger one.
- The idea for image hybridization is to combine a low-pass filtered image with another high-pass filtered image.
- First, transform the original image to the low-pass filtered image by using the gaussian_filter function. There is a parameter freq, which is called the “cutoff frequency”, controls how much frequency to leave in the transformed image and affects the blurriness of the low-pass filtered image.
- Then generate a high-pass filtered version of another image by subtracting a blurred version of the image itself.
- Finally, blend two images by adding them together.

    <div align=center>
    <img src="https://i.imgur.com/5jfwiqH.jpg" width=80%>
    </div>

### Experimental results

<div align=center>
<img src="https://i.imgur.com/9rnCfGt.jpg" width=80%>
<img src="https://i.imgur.com/DhGPAPz.jpg" width=80%>
<img src="https://i.imgur.com/thIutOP.jpg" width=80%>
<img src="https://i.imgur.com/ZYWyNVZ.jpg" width=80%>
</div>

## Task 2: Image Pyramid

### Implementation procedure

In task 2, we use a function named “transform.pyramid_gaussian()”. It is a function which is used to implement Gaussian Pyramid. The arguments of this function are the target image and the downscale, and it’s return value is the Gaussian Pyramid. Images in the Gaussian Pyramid are in descending order. We use for loop to output the images respectively and filter some low resolution images. Before we output the images, the answer have to be multiplied by 255 because the value of images was normalized to 0~1.

### Experimental results

- Marilyn Monroe

    <img src="https://i.imgur.com/PjqTzxq.jpg" width=50%>

- Cat Dog Hybrid Image

    <img src="https://i.imgur.com/xuiVEkA.jpg" width=70%>

- Fish

    <img src="https://i.imgur.com/c5fVntQ.jpg" width=70%>

- Lincoln Gala

    <img src="https://i.imgur.com/sLQwctk.jpg" width=70%>

## Task 3: Colorizing the Russian Empire

### Implementation procedure

For low resolution photos, we could just search over a window of possible displacements, and choose the displacement with best score, and then roll the image according to the best displacement. Here, we try to calculate score with both the Sum of Squared Differences (SSD). In this case, we choose the displacement window to have a size of 30px * 30px.

For high resolution pictures, exhaustive search may become unreasonable because it takes too much time. So instead, we use a search method called image pyramid . By rescaling the high-res photos to a reasonably small size, we could apply the single-scale alignment method recursively from smaller size photos to larger size.

We have noticed that the alignment of the photo called "Emir" is not successful at all. Because the feature we used is color. If we detect edges with Sobel Filter and use edges as a feature, the result would be much better.

![](https://i.imgur.com/AD3bLf7.png)


### Experimental results

![](https://i.imgur.com/E3V5BVN.jpg)

![](https://i.imgur.com/hroHedg.jpg)
