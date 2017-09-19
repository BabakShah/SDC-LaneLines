#importing some useful packages
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import glob
# %matplotlib inline

#reading in an image
#image = mpimg.imread('test_images/solidWhiteRight.jpg')
#printing out some stats and plotting
# print('This image is:', type(image), 'with dimesions:', image.shape)
# plt.imshow(image)  # if you wanted to show a single color channel image called 'gray', for example, call as plt.imshow(gray, cmap='gray')

import math


def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def region_of_interest(img, vertices):
    """
    Applies an image mask. Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    # defining a blank mask to start with
    mask = np.zeros_like(img)

    # defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    # filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    # returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, color=[255, 0, 0], thickness=8):
    """
    NOTE: this is the function you might want to use as a starting point once you want to
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).

    Think about things like separating line segments by their
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of
    the lines and extrapolate to the top and bottom of the lane.

    This function draws `lines` with `color` and `thickness`.
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.

    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img


# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., λ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.

    `initial_img` should be the image before any processing.

    The result image is computed as follows:

    initial_img * α + img * β + λ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, λ)

import os
# os.listdir("test_images")

images = glob.glob('test_input/*.jpg')

for i in range(len(images)):
    fig, axs = plt.subplots(2, 3)

    # img = mpimg.imread('test_images/solidYellowCurve2.jpg')
    img = mpimg.imread(images[i])
    axs[0,0].imshow(img)
    axs[0,0].set_title('Unprocessed Image', fontsize = 10)

    gray = grayscale(img)
    axs[0, 1].imshow(gray, cmap='gray')
    axs[0, 1].set_title('Grayscale Image', fontsize = 10)

    blur_gray = gaussian_blur(gray, 3)
    axs[0, 2].imshow(blur_gray, cmap='gray')
    axs[0, 2].set_title('Gaussian Kernel Image', fontsize = 10)

    edges = canny(blur_gray, 50, 150)
    axs[1, 0].imshow(edges, cmap='Greys_r')
    axs[1, 0].set_title('Canny Transform Image', fontsize = 10)

    imshape = img.shape
    vertices = np.array([[(0,imshape[0]),(460, 300), (470, 300), (imshape[1],imshape[0])]], dtype=np.int32)
    masked_image = region_of_interest(edges, vertices)
    axs[1, 1].imshow(masked_image, cmap='Greys_r')
    axs[1, 1].set_title('Masked Region Image', fontsize = 10)

    lines = hough_lines(masked_image, 1, np.pi/180, 1, 8, 1)
    results = weighted_img(lines, img)
    axs[1, 2].imshow(results)
    axs[1, 2].set_title('Hough Transform Image', fontsize = 10)

    fig.tight_layout()
    # mpimg.imsave("test-after.jpg", color_select)
    plt.imsave("test_output/test_after.jpg", results)
    plt.show()

    import imageio

    imageio.plugins.ffmpeg.download()
    # Import everything needed to edit/save/watch video clips
    from moviepy.editor import VideoFileClip
    from IPython.display import HTML


    def process_image(img):
        # NOTE: The output you return should be a color image (3 channel) for processing video below

        gray = grayscale(img)
        blur_gray = gaussian_blur(gray, 3)
        edges = canny(blur_gray, 50, 150)
        imshape = img.shape
        vertices = np.array([[(0, imshape[0]), (460, 300), (470, 300), (imshape[1], imshape[0])]], dtype=np.int32)
        masked_image = region_of_interest(edges, vertices)
        lines = hough_lines(masked_image, 1, np.pi / 180, 1, 8, 1)
        results = weighted_img(lines, img)
        return results


    white_output = 'test_output/white.mp4'
    clip1 = VideoFileClip("test_input/solidWhiteRight.mp4")
    white_clip = clip1.fl_image(process_image)  # NOTE: this function expects color images!!
    # % time white_clip.write_videofile(white_output, audio=False)

    HTML("""
    <video width="960" height="540" controls>
      <source src="{0}">
    </video>
    """.format(white_output))
