from ocr import recognize_text
from inference import *


def main(path_to_image, ocr_model):
    '''
    Recognize text and classificate words.

    Args:
        path_to_image (str):
            Path to image
        ocr_model (easyocr.Reader):
            OCR model
        ...
    Returns:
        ...
    '''
    ### OCR PART ###
    text = recognize_text(path_to_image, ocr_model)
    ### NER PART ### ....
    return get_predictions(text, model)
