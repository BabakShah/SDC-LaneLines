#Self-Driving Car Project: Finding Lane Lines on the Road

<img src="laneLines_thirdPass.jpg" width="480" alt="Combined Image" />

    One of the first things in developing a self-driving car is to automatically detect lane lines on the road using an algorithm in Pyhton and OpenCV.

**Contents** 
* Python script
* IPython notebook
* Test_input folder
* Test_output folder
* Readme file

### Reflection

### Pipeline:
The pipeline for detecting lane lines on the road is as follows:
1. Reading the input images from the test_input folder
2. Apply grayscale transform to convert RGB into grayscale
3. Reducing noise using Gaussian noise kernel
4. Apply Canny transform to get edges
5. Mask the image and apply region of interest
6. Apply Hough transform to find lines
7. Blending the Hough output image and the unprocessed image
8. Plotting and saving the output images into the test_output folder

Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline consisted of 5 steps. First, I converted the images to grayscale, then I .... 

In order to draw a single line on the left and right lanes, I modified the draw_lines() function by ...

If you'd like to include images to show how the pipeline works, here is how to include an image: 

![alt text][image1]


### shortcomings:


One potential shortcoming would be what would happen when ... 

Another shortcoming could be ...


### improvements:

A possible improvement would be to ...

Another potential improvement could be to ...
