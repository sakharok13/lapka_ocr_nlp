import torch
from transformers import pipeline

from .context import get_best_unions, get_correct_bounds, context_windows, intersects
from .model import model, tokenizer


def init_ner_model(gpu=True):
    ner_model = model()
    ner_tokenizer = tokenizer()
    if gpu:
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')
    ner_model.to(device)
    ner_model.eval()
    pipe = pipeline(model=ner_model,
                    tokenizer=ner_tokenizer,
                    task='ner',
                    aggregation_strategy='average',
                    device=0)
    return model, pipe


def get_predictions(data, model, pipe):

    windows, starts = context_windows(data)
    with torch.no_grad():
        preds = get_best_unions(get_correct_bounds(pipe, windows, starts), data)
    what_to_return = []
    for i in range(len(preds)):

        what_to_return.append( (preds[i]['entity_group'], preds[i]['word'], preds[i]['score']) )
    return what_to_return
