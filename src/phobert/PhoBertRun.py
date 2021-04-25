from pandas.io.parsers import PythonParser
import torch
import numpy as np
import pandas as pd
from config import SEED, PHOBERT_VERSION, EPOCHS, PATH_WEIGHT
from sklearn.model_selection import train_test_split
from PhoBertModel import PhoBertModel
import torch.optim as optim
from PhoBertTrainModel import phobert_train_model
from utils import loss_fn, phobert_get_train_val_loaders
from transformers import AutoTokenizer

np.random.seed(SEED)
torch.cuda.manual_seed(SEED)
torch.cuda.manual_seed_all(SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = True
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

data = pd.read_csv("./data/processed/train.csv")
train_df, val_df = train_test_split(data, test_size=0.2)
train_df = train_df.reset_index(drop=True)
val_df = val_df.reset_index(drop=True)

tokenizer = AutoTokenizer.from_pretrained(PHOBERT_VERSION)
model = PhoBertModel(PHOBERT_VERSION).to(device)

optimizer = optim.AdamW(model.parameters(), lr=3e-5, betas=(0.9, 0.999))
dataloaders_dict = phobert_get_train_val_loaders(train_df, val_df, tokenizer)
phobert_train_model(model, dataloaders_dict, EPOCHS,
                    optimizer, loss_fn,  PATH_WEIGHT, device)
