import cv2
from scripts.plate_detection import find_contours


def segment_characters(image):
    """
    This functions segments the characters from number plate and return those characters.
    :param image: image whose segmentation needs to be done.
    :return: characters
    """
    img = cv2.resize(image, (333, 75))

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('gray.jpg', img_gray)

    _, img_binary = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite('binary.jpg', img_binary)

    img_erode = cv2.erode(img_binary, (3, 3))
    cv2.imwrite('erode.jpg', img_erode)

    img_dilate = cv2.dilate(img_erode, (3, 3))
    cv2.imwrite('dilate.jpg', img_dilate)

    LP_WIDTH = img_dilate.shape[0]
    LP_HEIGHT = img_dilate.shape[1]

    img_dilate[0:3, :] = 255
    img_dilate[:, 0:3] = 255
    img_dilate[72:75, :] = 255
    img_dilate[:, 330:333] = 255

    dimensions = [LP_WIDTH / 6, LP_WIDTH / 2, LP_HEIGHT / 10, 2 * LP_HEIGHT / 3]

    char_list = find_contours(dimensions, img_dilate)

    return char_list
