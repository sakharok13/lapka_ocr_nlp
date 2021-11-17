from context import get_best_unions, get_correct_bounds, context_windows, intersects
from model import model, tokenizer
from transformers import pipeline
import torch

model = model()
tokenizer = tokenizer()
model.to('cpu')
model.eval()
pipe = pipeline(model=model,
                tokenizer=tokenizer,
                task='ner',
                aggregation_strategy='average',
                device=0)

def get_predictions(txtdata, model, pipe = pipe):

  windows, starts = context_windows(data)
  with torch.no_grad():
    preds = get_best_unions(get_correct_bounds(pipe, windows, starts), data)
  what_to_return = []
  for i in range(len(preds)):

    what_to_return.append( (preds[i]['entity_group'], preds[i]['word'], preds[i]['score']) )
  return what_to_return

