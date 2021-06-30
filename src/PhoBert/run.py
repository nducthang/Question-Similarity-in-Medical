import torch
from ruamel import yaml
import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer
from PhoBertModel import PhoBertModel
import torch.optim as optim
from PhoBertTrain import train
from utils import phobert_get_train_val_loaders, loss_fn

config = yaml.safe_load(open('./src/PhoBert/config.yaml'))

# config
torch.manual_seed(config['SEED'])
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load data
data = pd.read_csv(config['DATA_TRAIN'])
train_df, val_df = train_test_split(data, test_size=0.2)
train_df = train_df.reset_index(drop=True)
val_df = val_df.reset_index(drop=True)

# tokenizer and model, optimizer
tokenizer = AutoTokenizer.from_pretrained(config['PHOBERT_VERSION'])
model = PhoBertModel(config['PHOBERT_VERSION']).to(device)
optimizer = optim.AdamW(model.parameters(), lr=3e-5, betas=(0.9, 0.999))

dataloaders_dict = phobert_get_train_val_loaders(train_df, val_df, tokenizer, config)
train(model, dataloaders_dict, config['EPOCHS'], optimizer, loss_fn,  config, device)
