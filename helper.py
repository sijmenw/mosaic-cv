# created by Sijmen van der Willik
# 2019-04-19 13:47


import math

import cv2
import numpy as np
import matplotlib.pyplot as plt


def show_img(img, mode='large'):
    """Function to properly show different types of images, accepts binary, black and white and colour images

    :param img:
    :param mode:
    :return:
    """
    if np.max(img) <= 1:
        print("Showing as binary mask")
        if len(img.shape) > 2:
            img = np.max(img, axis=2)
        vmax = 1
    else:
        vmax = 255

    if mode == 'large':
        plt.figure(figsize=(20, 8))
    print("Image size:{}".format(img.shape))
    if len(img.shape) == 3:
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    else:
        plt.imshow(img, cmap='gray', vmin=0, vmax=vmax)


def flex_combine(images, shape=None, h_pad=10, v_pad=10):
    """resizes every image to size of the largest image

    added portions are coloured gray

    :param images:
    :param shape:
    :param h_pad:
    :param v_pad:
    :return: <numpy array>
    """
    max_h = 0
    max_w = 0
    gray = (210, 210, 210)

    for im in images:
        if im.shape[0] > max_h:
            max_h = im.shape[0]
        if im.shape[1] > max_w:
            max_w = im.shape[1]

    canvas = np.full((max_h, max_w, 3), gray)

    res = []

    for i in range(len(images)):
        tmp = np.copy(canvas)
        tmp[:images[i].shape[0], :images[i].shape[1]] = images[i]
        res.append(tmp)

    return combine_img(res, shape=shape, h_pad=h_pad, v_pad=v_pad)


def combine_img(images, shape=None, h_pad=10, v_pad=10):
    """combines all images into one image

    assumes all images are the same size

    :param images: <iterable of images>
    :param shape: <list or tuple, int> number of rows, number of columns of resulting grid
        if input is int, the it interpreted as width
        when tuple or list, one value can be -1, it will be changed to smallest fit
    :param h_pad:
    :param v_pad:
    :return: a single image combining all images
    """
    images = np.array(images)
    im_h = images.shape[1]
    im_w = images.shape[2]
    if shape is None:
        grid_w = 4
        grid_h = math.ceil(images.shape[0] / grid_w)
    elif type(shape) is int:
        grid_w = shape
        grid_h = math.ceil(images.shape[0] / grid_w)
    elif shape[1] == -1:
        grid_w = shape[0]
        grid_h = math.ceil(images.shape[0] / grid_w)
    elif shape[0] == -1:
        grid_h = shape[1]
        grid_w = math.ceil(images.shape[0] / grid_h)
    else:
        grid_w = shape[1]
        grid_h = shape[0]

    canvas = np.zeros((grid_h * im_h + (grid_h - 1) * v_pad,
                       grid_w * im_w + (grid_w - 1) * h_pad,
                       images.shape[3]), dtype=np.uint8)

    for i in range(images.shape[0]):
        x = i % grid_w
        y = i // grid_w
        x1 = x * (im_w + h_pad)
        x2 = x1 + im_w
        y1 = y * (im_h + v_pad)
        y2 = y1 + im_h
        canvas[y1:y2, x1:x2] = images[i]

    return canvas
