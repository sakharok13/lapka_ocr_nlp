def context_windows(string, window = 150, stride = 100):
  text = string.split(sep=' ')

  windows = []
  start = []

  for k in range(len(text) // stride):
    if len(text[k * stride:]) >= window:
      stroka = ' '.join(text[k * stride : k * stride + window])
      windows.append(stroka)
      start.append(string.find(stroka))
    else:
      stroka = ' '.join(text[k * stride :])
      windows.append(stroka)
      start.append(string.find(stroka))

  return windows, start

def get_correct_bounds(pipe, windows, starts):
  answers = []

  for i, win in enumerate(windows):
    dic = pipe(win)
    for d in dic:
      d['start'] += starts[i]
      d['end'] += starts[i]
    answers.append(dic)
  return answers

def intersects(uni, d):
  if uni['start'] >= d['start'] and uni['start'] <= d['end']:

    uni['start'] = d['start']
    uni['end'] = max(uni['end'], d['end'])
    return uni

  elif d['start'] >= uni['start'] and d['end'] >= uni['end'] and d['start'] <= uni['end']:

    uni['end'] = d['end']
    return uni

  else:
    return False

def get_best_unions(dics, text):
  union = []

  for d in range(len(dics)):
    for dic in dics[d]:

      if len(union) == 0 or intersects(union[-1], dic) == False:
        union.append(dic)
      else:
        union[-1] = intersects(union[-1], dic)
  for k in union:
    k['word'] = text[k['start'] : k['end']]
  
  return union
