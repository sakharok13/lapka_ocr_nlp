import easyocr
import cv2
import numpy as np
from scipy.ndimage import interpolation as inter


def init_ocr_model(gpu=True):
    '''
    Init OCR model.

    Args:
        gpu (bool):
            Whether to use GPU
    Returns:
        model (easyocr.Reader):
            OCR model
    '''
    recognizer = easyocr.Reader(['ru', 'en'], gpu=gpu)
    return recognizer


def remove_shadow(img):
  '''
  Remove shadow from image.

  Args:
      img (np.ndarray):
          Numpy array of image
  Returns:
      img (np.ndarray):
          Image with removed shadow
  '''
  rgb_planes = cv2.split(img)
  result_planes = []
  result_norm_planes = []
  for plane in rgb_planes:
      dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
      bg_img = cv2.medianBlur(dilated_img, 21)
      diff_img = 255 - cv2.absdiff(plane, bg_img)
      norm_img = cv2.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
      result_planes.append(diff_img)
      result_norm_planes.append(norm_img)
  result = cv2.merge(result_planes)
  result_norm = cv2.merge(result_norm_planes)
  return result_norm


def correct_skew(image, delta=1, limit=5):
    '''
    Correct image skew.

    Args:
        image (np.ndarray):
            Numpy array of image
        delta (int):
            Step of angle search
        limit (int):
            Limit of angle search
    Returns:
        image (np.ndarray):
            Image with corrected skew
    '''
    def determine_score(arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2)
        return histogram, score

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] 

    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    for angle in angles:
        histogram, score = determine_score(thresh, angle)
        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, \
              borderMode=cv2.BORDER_REPLICATE)
    return rotated


def recognize_text(path_to_image, recognizer):
    '''
    Recognize text on image.

    Args:
        path_to_image (str): 
            Path to image to recognize
        recognizer (easyocr.Reader): 
            EasyOCR image recognizer
    Returns:
        text (str):
            Recognized text
    '''
    image = cv2.imread(path_to_image)
    image = remove_shadow(image)
    image = correct_skew(image)
    text = ' '.join(recognizer.readtext(image, detail=0, paragraph=True))
    return text