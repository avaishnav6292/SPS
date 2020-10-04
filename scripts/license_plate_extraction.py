import cv2


def extract_plate(img):
    """
    This function extracts number plate from an image and return image with plate and plate alone.
    :param img: image in which number plate needs to be detected.
    :return: plate_image, plate
    """
    plate_img = img.copy()

    classifier_path = '/home/dshakya29/projects/number_plate_detection/scripts/cascade/indian_license_plate.xml'

    plate_cascade = cv2.CascadeClassifier(classifier_path)
    plate_rect = plate_cascade.detectMultiScale(plate_img, scaleFactor=1.5, minNeighbors=7)

    plate = None

    for (x, y, w, h) in plate_rect:
        a, b = (int(0.02 * img.shape[0]), int(0.025 * img.shape[1]))
        plate = plate_img[y + a:y + h - a, x + b:x + w - b, :]
        cv2.rectangle(plate_img, (x, y), (x + w, y + h), (51, 51, 255), 3)

    return plate_img, plate
