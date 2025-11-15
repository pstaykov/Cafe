from data import load_dataset, tokenize_texts, build_vocab, encode_and_pad, split_data
from train import train_model
from predict import load_model, predict_sentence, append_to_dataset
import os

MODEL_PATH = "sentiment_model_full.pth"

mode = input("train or test? ").strip().lower()

if mode == "train":
    texts, labels = load_dataset()
    tokenized = tokenize_texts(texts)
    vocab = build_vocab(tokenized)
    padded, max_len = encode_and_pad(tokenized, vocab)
    train_text, train_labels, val_text, val_labels = split_data(padded, labels)

    train_model(train_text, train_labels, val_text, val_labels, vocab, max_len, MODEL_PATH)

else:  # test mode
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Train first.")
        exit()

    model, vocab, max_len = load_model(MODEL_PATH)

    # user input
    text = input("Enter a sentence: ")

    pred = predict_sentence(model, vocab, max_len, text)
    print("\nPredicted:", "Positive" if pred == 1 else "Negative")

    # ask real label
    actual = input("\nActual sentiment? (0=neg, 1=pos): ")
    append_to_dataset(text, actual)
