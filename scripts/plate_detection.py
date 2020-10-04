import cv2
import numpy as np


def find_contours(dimensions, img):
    """
    This function find contours consisting of plate.
    :param dimensions:
    :param img: Image in which contours need to be find.
    :return: image with contours.
    """
    contours, _ = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    lower_width = dimensions[0]
    upper_width = dimensions[1]
    lower_height = dimensions[2]
    upper_height = dimensions[3]

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]

    x_contours_list = []
    img_res = []

    for contour in contours:
        intX, intY, intWidth, intHeight = cv2.boundingRect(contour)

        if lower_width < intWidth < upper_width and lower_height < intHeight < upper_height:
            x_contours_list.append(intX)

            char_copy = np.zeros((44, 24))

            char = img[intY:intY + intHeight, intX:intX + intWidth]
            char = cv2.resize(char, (20, 40))

            char = cv2.subtract(255, char)

            char_copy[2:42, 2:22] = char
            char_copy[0:2, :] = 0
            char_copy[:, 0:2] = 0
            char_copy[42:44, :] = 0
            char_copy[:, 22:24] = 0

            img_res.append(char_copy)

    indices = sorted(range(len(x_contours_list)), key=lambda k: x_contours_list[k])

    img_res_copy = []

    for idx in indices:
        img_res_copy.append(img_res[idx])

    img_res = np.array(img_res_copy)

    return img_res
