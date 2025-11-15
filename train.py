import torch
import torch.nn as nn
import json
from model import SentimentAnalysisModel
from nltk.tokenize import word_tokenize
from collections import Counter
import time

# Load dataset
with open("texts.json","r",encoding="utf-8") as f:
    data = json.load(f)["data"]

texts = [d["text"] for d in data]
labels = [d["label"] for d in data]

tokens = [word_tokenize(t.lower()) for t in texts]
vocab = {"<PAD>":0,"<UNK>":1}

counter = Counter([w for t in tokens for w in t])
for i,(w,_) in enumerate(counter.items(),start=2):
    vocab[w] = i

indexed = [[vocab.get(w,1) for w in t] for t in tokens]
max_len = max(len(i) for i in indexed)
padded = [i+[0]*(max_len-len(i)) for i in indexed]

X = torch.tensor(padded)
y = torch.tensor(labels)

model = SentimentAnalysisModel(vocab_size=len(vocab), embed_dim=50)
criterion = nn.CrossEntropyLoss()
optim = torch.optim.Adam(model.parameters(), lr=0.003)

for epoch in range(8):
    optim.zero_grad()
    preds = model(X)
    loss = criterion(preds, y)
    loss.backward()
    optim.step()
    print("Epoch",epoch,"Loss",loss.item())

# Save model with timestamp
fname = f"sentiment_model_{int(time.time())}.pth"
torch.save({
    "model_state": model.state_dict(),
    "vocab": vocab,
    "max_len": max_len
}, fname)

print("Saved new model:", fname)
