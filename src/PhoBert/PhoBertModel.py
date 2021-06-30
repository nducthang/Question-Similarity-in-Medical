from transformers import AutoModel
import torch.nn as nn


class PhoBertModel(nn.Module):
    def __init__(self, phobert_path):
        super(PhoBertModel, self).__init__()
        self.phobert_path = phobert_path
        self.phobert = AutoModel.from_pretrained(self.phobert_path)
        self.dropout = nn.Dropout(0.3)
        self.out = nn.Linear(768, 1)

    def forward(self, ids, mask, token_type_ids):
        _, pooled = self.phobert(
            ids, attention_mask=mask, token_type_ids=token_type_ids)
        # add dropout to prevent overfitting
        pooled = self.dropout(pooled)
        return self.out(pooled)
