import musx
import musx_images
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def function_template():
    """<description>

    Arguments:
        <arg>: <desc>
    
    Returns/Yields:
        <desc>
    
    Raises:
        <exception>: <desc>
    """

    return None

# ---------------- #
# Helper Functions #
# ---------------- #

def load_image(image_path, *, color_space="RGB"):
    """Loads an image from a path into a matrix of data.

    Arguments:
        image_path: string, filepath to the desired image to be loaded
        color_space: string, color space data to receive, defaults to RGB
    
    Returns/Yields:
        3D number Numpy array, whose dimensions represent x-coord, y-coord, channel
    """
    img_BGR = cv.imread(image_path)

    return convert_image(img_BGR, color_space=color_space)


def convert_image(img, *, color_space="RGB"):
    """Converts an image from the BGR color space to the specified color space

    Arguments:
        img: 3D number Numpy array, data representation of image
        color_space: string, color space to convert from BGR (OpenCV's loading standard), defaults to RGB
    
    Returns/Yields:
        3D number Numpy array, representing the image in the correct colorspace
    """
    if color_space == "BGR": # Blue, green, red, see RGB below
        converted_img = img
    elif color_space == "Gray": # Grayscale, special treatment for matplotlib plotting
        converted_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    elif color_space == "HLS": # Hue (0-180), lightness, saturation, see https://en.wikipedia.org/wiki/HSL_and_HSV
        converted_img = cv.cvtColor(img, cv.COLOR_BGR2HLS)
    elif color_space == "HLS_FULL": # Hue (0-255), lightness, saturation, see https://en.wikipedia.org/wiki/HSL_and_HSV
        converted_img = cv.cvtColor(img, cv.COLOR_BGR2HLS_FULL)
    elif color_space == "HSV": # Hue (0-180), saturation, value, see https://en.wikipedia.org/wiki/HSL_and_HSV
        converted_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    elif color_space == "HSV_FULL": # Hue (0-255), saturation, value, see https://en.wikipedia.org/wiki/HSL_and_HSV
        converted_img = cv.cvtColor(img, cv.COLOR_BGR2HSV_FULL)
    elif color_space == "Lab": # CIELAB color space, see https://en.wikipedia.org/wiki/CIELAB_color_space
        converted_img = cv.cvtColor(img, cv.COLOR_BGR2Lab)
    elif color_space == "Luv": # CIELUV color space, see https://en.wikipedia.org/wiki/CIELUV
        converted_img = cv.cvtColor(img, cv.COLOR_BGR2Luv)
    elif color_space == "RGB": # Red, green, blue, see https://en.wikipedia.org/wiki/RGB_color_space
        converted_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    elif color_space == "XYZ": # CIE 1931 XYZ color space, see https://en.wikipedia.org/wiki/CIE_1931_color_space
        converted_img = cv.cvtColor(img, cv.COLOR_BGR2XYZ)
    elif color_space == "YCbCr": # Luma, blue-diff, red-diff, see https://en.wikipedia.org/wiki/YCbCr
        converted_img = cv.cvtColor(img, cv.COLOR_BGR2YCrCb)
    elif color_space == "YUV": # YUV color space, see https://en.wikipedia.org/wiki/YUV
        converted_img = cv.cvtColor(img, cv.COLOR_BGR2YUV)
    elif color_space == "YUV_IYUV": # not sure, seems to add extra information to image?
        converted_img = cv.cvtColor(img, cv.COLOR_BGR2YUV_IYUV)
    elif color_space == "YUV_I420": # not sure, seems to add extra information to image?
        converted_img = cv.cvtColor(img, cv.COLOR_BGR2YUV_I420)
    elif color_space == "YUV_YV12": # not sure, seems to add extra information to image?
        converted_img = cv.cvtColor(img, cv.COLOR_BGR2YUV_YV12)
    
    return converted_img

# --------------- #
# Data Generators #
# --------------- #

def image_data(*, image_path, stop=None, color_space="RGB", start_x=0, start_y=0, movement="x:i y:i"):
    """<description>

    Arguments:
        <arg>: <desc>
    
    Returns/Yields:
        <desc>
    
    Raises:
        <exception>: <desc>
    """

    return None