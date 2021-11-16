label_list = ['I-Диагноз',
 'I-Дозировка',
 'I-Кличка',
 'I-Назначенные лекарства',
 'I-Симптомы',
 'I-Сколько пить',
 'O']

def tokenize_and_align_labels(examples, label_all_tokens=True):
    tokenized_inputs = tokenizer(examples['tokens'], truncation=True, is_split_into_words=True)

    labels = []
    for i, label in enumerate(examples['tags']):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:

            if word_idx is None:
                label_ids.append(-100)

            elif word_idx != previous_word_idx:
                label_ids.append(label[word_idx])

            else:
                label_ids.append(label[word_idx] if label_all_tokens else -100)
            previous_word_idx = word_idx

        label_ids = [label_list.index(idx) if isinstance(idx, str) else idx for idx in label_ids]

        labels.append(label_ids)

    tokenized_inputs["labels"] = labels
    return tokenized_inputs


from transformers import AutoModelForTokenClassification, AutoTokenizer
def model():
    bert = AutoModelForTokenClassification.from_pretrained("sakharok/lapka", num_labels=len(label_list))
    bert.config.id2label = dict(enumerate(label_list))
    bert.config.label2id = {v: k for k, v in model.config.id2label.items()}
    return bert
def tokenizer():
    return AutoTokenizer.from_pretrained('DeepPavlov/rubert-base-cased')
