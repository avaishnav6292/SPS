import numpy as np
import cv2
from keras.models import load_model
from scripts.license_plate_extraction import extract_plate
from scripts.character_segmentation import segment_characters


def fix_dimension(img):
    new_img = np.zeros((28, 28, 3))
    for i in range(3):
        new_img[:, :, i] = img
    return new_img


def show_results(model, chars_list):
    dic = {}
    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXY2'
    for i, c in enumerate(characters):
        dic[i] = c

    output = []

    for i, ch in enumerate(chars_list[:10]):
        img_ = cv2.resize(ch, (28, 28))
        img = fix_dimension(img_)
        img = img.reshape(1, 28, 28, 3)
        y_ = model.predict_classes(img)[0]
        character = dic[y_]
        output.append(character)

    plate_number = ''.join(output)

    return plate_number


def get_plate_number(image_link):
    model = load_model('model.h5')
    image = cv2.imread(image_link)
    plate_img, plate = extract_plate(image)
    cv2.imwrite('image_with_plate.jpg', plate_img)
    cv2.imwrite('plate.jpg', plate)
    chars = segment_characters(plate)
    number = show_results(model, chars)
    return number
