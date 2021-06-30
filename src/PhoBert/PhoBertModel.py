from os import setxattr
from transformers import AutoModel
import torch.nn as nn


class PhoBertModel(nn.Module):
    def __init__(self, phobert_path):
        super(PhoBertModel, self).__init__()
        self.phobert_path = phobert_path
        self.phobert = AutoModel.from_pretrained(self.phobert_path, return_dict = False)
        self.dropout = nn.Dropout(0.3)
        self.fc1 = nn.Linear(768, 384)
        self.fc2 = nn.Linear(384, 1)

    def forward(self, ids, mask, token_type_ids):
        _, pooled = self.phobert(ids, attention_mask=mask, token_type_ids=token_type_ids)
        # add dropout to prevent overfitting
        fc1 = self.fc1(pooled)
        fc2 = self.dropout(self.fc2(fc1))
        return fc2
