import musx
import musx_images
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import sys

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

valid_color_spaces = ["BGR", "Gray", "HLS", "HLS_FULL", "HSV", "HSV_FULL", "Lab", "Luv", "RGB", "XYZ", "YCbCr", "YUV"]



# ---------------- #
# Helper Functions #
# ---------------- #

def load_image(image_path, *, color_space="RGB"):
    """Loads an image from a path into a matrix of data.

    Arguments:
        image_path: string, filepath to the desired image to be loaded
        color_space: string, color space data to receive, defaults to RGB
    
    Returns:
        3D number Numpy array, whose dimensions represent x-coord, y-coord, channel
    
    Raises:
        ValueError: specified color space is not supported
    """
    if color_space not in valid_color_spaces:
        raise ValueError ("Specified color space '{}' is not in supported list of color spaces: {}".format(color_space, ', '.join(valid_color_spaces)))

    img_BGR = cv.imread(image_path)

    return convert_image(img_BGR, color_space=color_space)


def convert_image(img, *, color_space="RGB"):
    """Converts an image from the BGR color space to the specified color space.
    If the base image is not in the BGR color space, then this can lead to some weird behavior.

    Arguments:
        img: 3D number Numpy array, data representation of image to convert
        color_space: string, color space to convert from BGR (OpenCV's loading standard), defaults to RGB
    
    Returns:
        3D number Numpy array, representing the image in the correct colorspace
    
    Raises:
        ValueError: specified color space is not supported
    """

    if color_space not in valid_color_spaces:
        raise ValueError ("Specified color space '{}' is not in supported list of color spaces: {}".format(color_space, ', '.join(valid_color_spaces)))

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


def randomize_color_space(img, iterations=1, *, final_color_space=None):
    """Converts an image into a random three channel color space.

    Arguments:
        img: 3D number Numpy array, data representation of image to randomize color space
        iterations: int, number of random color space transforms, defaults to 1
        final_color_space: string, if specified, reduces number of random iterations by 1 and finishes with the specified color space
    
    Returns:
        3D number Numpy array, representing an image in a mangled color space
    
    Raises:
        ValueError: nonsense iterations number or specified final color space is not supported
    """
    if iterations <= 0:
        raise ValueError ("Number of iterations must be 1 or greater")

    rand_color_space = musx.choose(musx_images.valid_color_spaces)

    if final_color_space != None:
        if final_color_space not in valid_color_spaces:
            raise ValueError ("Specified final color space '{}' is not in supported list of color spaces: {}".format(color_space, ', '.join(valid_color_spaces)))
        adjusted_iterations = iterations - 1
    else:
        adjusted_iterations = iterations
    
    converted_img = img.copy()
    for i in range(adjusted_iterations):
        color_space = next(rand_color_space)

        while color_space == "Gray": # Prevent grayscale transformation as it is only 1 channel
            color_space = next(rand_color_space)

        converted_img = convert_image(converted_img, color_space=color_space)
    
    if final_color_space != None:
        converted_img = convert_image(converted_img, color_space=final_color_space)
    
    return converted_img



# --------------- #
# Data Generators #
# --------------- #

def traversal_2d(items, *, stop=None, start_x=0, start_y=0, movement=[(1, 0), (0, 1)]):
    """Traverses a two dimensional list / numpy array according to movement rules.
    If the first movement rule walks off the array, the second movement rule is used
    and the indices wrap using the % operator.

    Arguments:
        items: 2D list / 2D numpy array, items to walk through
        stop: int, number of items to yield, defaults to infinite*
        start_x: int, starting location in the first dimension, defaults to 0
        start_y: int, starting location in the second dimension, defaults to 0
        movement: list of two pairs, specifies dimensional movement, defaults to row-major
    
    Yields:
        Information at the given location
    
    Raises:
        TODO: error handling for bad dimension sizes, negative stop size
    """

    np_items = np.array(items)

    if stop == None:
        stop = sys.maxsize

    x_pos = start_x
    y_pos = start_y

    yield list(np_items[x_pos, y_pos]) # Yield original item

    for _ in range(stop - 1):
        x_pos += movement[0][0]
        y_pos += movement[0][1]

        # Use second movement rule if off bounds
        if x_pos >= np_items.shape[0] or x_pos < 0 or y_pos >= np_items.shape[1] or y_pos < 0:
            x_pos += movement[1][0]
            y_pos += movement[1][1]
        
        x_pos %= np_items.shape[0]
        y_pos %= np_items.shape[1]

        yield list(np_items[x_pos, y_pos])