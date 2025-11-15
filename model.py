import torch.nn as nn
import torch.nn.functional as F

class SentimentAnalysisModel(nn.Module):
    def __init__(self, vocab_size, embed_dim=50):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.conv = nn.Conv1d(embed_dim, embed_dim, kernel_size=3, padding=1)
        self.dropout = nn.Dropout(0.5)
        self.fc = nn.Linear(embed_dim, 2)

    def forward(self, text):
        embedded = self.embedding(text).permute(0, 2, 1)
        conved = F.relu(self.conv(embedded))
        pooled = conved.mean(dim=2)
        dropped = self.dropout(pooled)
        return self.fc(dropped)
