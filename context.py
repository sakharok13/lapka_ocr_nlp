
def context_windows(string, window = 200, stride = 40):
  text = string.split()

  windows = []

  if len(text) <= window:
    windows.append(i)

  else:
    starts = []

    for k in range(len(text) // stride):
      if len(text[k * stride:]) >= window:
        stroka = ' '.join(text[k * stride : k * stride + window])
        windows.append(stroka)
        starts.append(string.find(stroka))
      else:
        stroka = ' '.join(text[k * stride :])
        windows.append(stroka)
        starts.append(string.find(stroka))

  return windows, starts

def get_correct_bounds(pipe, windows, starts):
  answers = []

  for i, win in enumerate(windows):
    dic = pipe(win)
    for d in dic:
      d['start'] += starts[i]
      d['end'] += starts[i]
    answers.append(dic)
  return answers

