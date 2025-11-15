import json
import torch
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from collections import Counter

def load_dataset(path="texts.json"):
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    texts = [d["text"] for d in raw["data"]]
    labels = [d["label"] for d in raw["data"]]
    return texts, labels

def tokenize_texts(texts):
    return [word_tokenize(t.lower()) for t in texts]

def build_vocab(tokenized):
    freq = Counter([w for text in tokenized for w in text])
    vocab = {"<PAD>": 0, "<UNK>": 1}
    for word, _ in freq.most_common():
        vocab[word] = len(vocab)
    return vocab

def encode_and_pad(tokenized, vocab):
    indexed = [[vocab.get(w, 1) for w in text] for text in tokenized]
    max_len = max(len(x) for x in indexed)
    padded = [x + [0]*(max_len - len(x)) for x in indexed]
    return padded, max_len

def split_data(padded, labels):
    idx_train, idx_val = train_test_split(
        range(len(padded)), test_size=0.2,
        stratify=labels, random_state=42
    )
    train_text = torch.tensor([padded[i] for i in idx_train])
    train_labels = torch.tensor([labels[i] for i in idx_train])
    val_text = torch.tensor([padded[i] for i in idx_val])
    val_labels = torch.tensor([labels[i] for i in idx_val])
    return train_text, train_labels, val_text, val_labels
