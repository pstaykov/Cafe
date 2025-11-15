import torch
from model import SentimentAnalysisModel
from nltk.tokenize import word_tokenize

import nltk
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")


def load_model(path):
    """
    Loads the saved PyTorch model + vocab + max_len
    """
    checkpoint = torch.load(path, map_location="cpu")

    vocab = checkpoint["vocab"]
    max_len = checkpoint["max_len"]

    model = SentimentAnalysisModel(vocab_size=len(vocab), embed_dim=50)
    model.load_state_dict(checkpoint["model_state"])
    model.eval()

    return model, vocab, max_len


def preprocess_text(text, vocab, max_len):
    """
    Tokenizes + pads text for prediction
    """
    tokens = word_tokenize(text.lower())
    idxs = [vocab.get(w, vocab["<UNK>"]) for w in tokens]

    if len(idxs) < max_len:
        idxs += [0] * (max_len - len(idxs))
    else:
        idxs = idxs[:max_len]

    return torch.tensor([idxs])


def predict_text(text, model, vocab, max_len):
    """
    Runs the model and returns (sentiment_string, label_int)
    """

    input_tensor = preprocess_text(text, vocab, max_len)

    with torch.no_grad():
        out = model(input_tensor)
        pred_label = torch.argmax(out, dim=1).item()

    sentiment = "Positive" if pred_label == 1 else "Negative"

    return sentiment, pred_label
