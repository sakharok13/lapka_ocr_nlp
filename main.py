from ocr import recognize_text
from ner import get_predictions


def main(path_to_image, ocr_model, ner_model, ner_pipeline):
    '''
    Recognize text and classificate words.

    Args:
        path_to_image (str):
            Path to image
        ocr_model (easyocr.Reader):
            OCR model
        ner_model (torch.nn.Module):
            NER model
        ner_pipeline (transformers.pipelines.base.Pipeline):
            NER pipeline
    '''
    ### OCR PART ###
    text = recognize_text(path_to_image, ocr_model)
    ### NER PART ###
    prediction = get_predictions(text, ner_model, ner_pipeline)
    return prediction
