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

# ------------------------ #
# Library Global Variables #
# ------------------------ #

valid_color_spaces = ["BGR", "Gray", "HLS", "HLS_FULL", "HSV", "HSV_FULL", "Lab", "Luv", "RGB", "XYZ", "YCbCr", "YUV"]



# ------------------------ #
# Image Specific Functions #
# ------------------------ #

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


def display_image(img, *, grayscale=False):
    """Wrapper on matplotlib's imshow function.

    Arguments:
        img: 3D number Numpy array, image to display, assumes RGB format
        grayscale: boolean, flag for if image is grayscale or not, defaults to False
    """
    fig, axes = plt.subplots(1, 1, figsize=(10, 10))

    if grayscale:
        axes.imshow(img, cmap='gray')
    else:
        axes.imshow(img)



def display_points(img, points, *, grayscale=False):
    """Plots points alongside the original image.

    Arguments:
        img: 3D number Numpy array, image to display, assumes RGB format
        points: list of number pairs, points to plot
        grayscale: boolean, flag for if image is grayscale or not, defaults to False
    """
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))
    
    plt1 = axes[0]
    if grayscale:
        plt1.imshow(img, cmap='gray')
    else:
        plt1.imshow(img)
    
    plt2 = axes[1]
    points_image = np.empty_like(img)
    points_image.fill(255)

    for (x, y) in points:
        points_image[max(0, x - 25):min(img.shape[0] - 1, x + 25),max(0, y - 25):min(img.shape[1] - 1, y + 25)] = img[max(0, x - 25):min(img.shape[0] - 1, x + 25),max(0, y - 25):min(img.shape[1] - 1, y + 25)]

    plt2.imshow(points_image)




# ------------------ #
# Resizing Functions #
# ------------------ #

def avg_pool_2d():
    raise NotImplementedError


def min_pool_2d():
    raise NotImplementedError


def max_pool_2d():
    raise NotImplementedError


def kerneling():
    raise NotImplementedError


def linear_interp_2d():
    raise NotImplementedError



# ------------- #
# 2D Generators #
# ------------- #

def traversal_2d(items, stop=None, *, start_row=0, start_col=0, movement=[(0, 1), (1, 0)]):
    """Traverses a two dimensional list / numpy array according to movement rules.
    If the first movement rule walks off the array, the second movement rule is used
    and the indices wrap using the % operator.

    Arguments:
        items: 2D list / 2D numpy array, items to walk through
        stop: int, number of items to yield, defaults to infinite*
        start_row: int, starting location in the first dimension, defaults to 0
        start_col: int, starting location in the second dimension, defaults to 0
        movement: list of two pairs, specifies dimensional movement, defaults to row-major
    
    Yields:
        Information at the given location, coordinates
    
    Raises:
        TODO: error handling for bad dimension sizes, negative stop size
    """

    np_items = np.array(items)

    if stop == None:
        stop = sys.maxsize

    row = start_row
    col = start_col

    yield list(np_items[row, col]), (row, col) # Yield original item

    for _ in range(stop - 1):
        row += movement[0][0]
        col += movement[0][1]

        # Use second movement rule if off bounds
        if row >= np_items.shape[0] or row < 0 or col >= np_items.shape[1] or col < 0:
            row += movement[1][0]
            col += movement[1][1]
        
        row %= np_items.shape[0]
        col %= np_items.shape[1]

        yield list(np_items[row, col]), (row, col)


def drunk_2d(items, stop=None, *, start_row=0, start_col=0, width=(1, 1), movement_2d=True, mode="wrap"):
    """Drunkenly walks along a two dimensional list / numpy array.
    Based off of musx.generators.drunk.

    Arguments:
        items: 2D list / 2D numpy array, items to walk through
        stop: int, number of items to yield, defaults to infinite*
        start_row: int, starting location in the first dimension, defaults to 0
        start_col: int, starting location in the second dimension, defaults to 0
        width: pair of ints, specifies range of dimensional movement, defaults to one in both dimensions
        movement_2d: boolean, whether movement in both dimensions at same time is possible, defaults to True
        mode: string, how to handle out of bounds (see musx.tools.fit), defaults to wrapping around
    
    Yields:
        Information at the given location, coordinates
    
    Raises:
        TODO: error handling
    """
    np_items = np.array(items)

    if stop == None:
        stop = sys.maxsize

    row = start_row
    col = start_col

    yield list(np_items[row, col]), (row, col) # Yield original item

    row_deviation = musx.choose([x for x in range(-1 * width[0], width[0] + 1)])
    col_deviation = musx.choose([x for x in range(-1 * width[1], width[1] + 1)])

    for _ in range(stop - 1):
        if movement_2d == False:
            if musx.odds(0.5):
                row += next(row_deviation)
            else:
                col += next(col_deviation)
        else:
            row += next(row_deviation)
            col += next(col_deviation)

        row = musx.fit(row, 0, items.shape[0], mode=mode)
        col = musx.fit(col, 0, items.shape[1], mode=mode)

        yield list(np_items[row, col]), (row, col)


def random_2d(items, stop=None):
    """Randomly picks elements of a two dimensional list / numpy array.

    Arguments:
        items: 2D list / 2D numpy array, items to walk through
        stop: int, number of items to yield, defaults to infinite*
    
    Yields:
        Information at the given location, coordinates
    
    Raises:
        TODO: error handling
    """
    np_items = np.array(items)

    if stop == None:
        stop = sys.maxsize

    for _ in range(stop):

        row = round(musx.uniran() * items.shape[0])
        col = round(musx.uniran() * items.shape[1])

        yield list(np_items[row, col]), (row, col)


def distribution_2d(items, stop=None, *, row_distribution=musx.gauss, row_dist_low=-4, row_dist_high=4, col_distribution=musx.gauss, col_dist_low=-4, col_dist_high=4):
    """Picks elements of a two dimensional list / numpy array according to a specified distribution.

    Arguments:
        items: 2D list / 2D numpy array, items to walk through
        stop: int, number of items to yield, defaults to infinite*
        row_distribution: function returning a number, distribution for row axis
        row_dist_low: number, lower bound on row_distribution function
        row_dist_high: number, upper bound on row_distribution function
        col_distribution: function returning a number, distribution for column axis
        col_dist_low: number, lower bound on col_distribution function
        col_dist_high: number, upper bound on col_distribution function
    
    Yields:
        Information at the given location, coordinates
    
    Raises:
        TODO: error handling
    """
    np_items = np.array(items)

    if stop == None:
        stop = sys.maxsize

    for _ in range(stop):

        row_raw = musx.fit(row_distribution(), row_dist_low, row_dist_high)
        col_raw = musx.fit(col_distribution(), col_dist_low, col_dist_high)

        row = round(musx.rescale(row_raw, row_dist_low, row_dist_high, 0, items.shape[0]))
        col = round(musx.rescale(col_raw, col_dist_low, col_dist_high, 0, items.shape[1]))

        yield list(np_items[row, col]), (row, col)


def line_2d(items, stop=None, *, start_row, start_col, end_row, end_col, step_size=1):
    np_items = np.array(items)

    if stop == None:
        stop = sys.maxsize

    exact_row = start_row
    exact_col = start_col

    yield list(np_items[exact_row, exact_col]), (exact_row, exact_col) # Yield original item

    # TODO: fix this
    row_step = (end_row - start_row) / step_size
    col_step = (end_col - start_col) / step_size

    for i in range(stop - 1):
        if i < 10:
            print("hi")
        exact_row += row_step
        exact_col += col_step

        row = round(exact_row)
        col = round(exact_col)

        yield list(np_items[row, col]), (row, col)

        if row == end_row and col == end_col:
            break

def path_2d(items, *, start_row, start_col, end_x, end_y, max_len=None):
    raise NotImplementedError