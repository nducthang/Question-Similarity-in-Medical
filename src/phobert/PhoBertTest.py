import torch
from PhoBertModel import PhoBertModel
from transformers import AutoTokenizer
from config import SEED, PHOBERT_VERSION, PATH_WEIGHT
import numpy as np
import pandas as pd
from PhoBertDataset import PhoBertDataset
import tqdm
import torch.nn as nn

np.random.seed(SEED)
torch.cuda.manual_seed(SEED)
torch.cuda.manual_seed_all(SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = True
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(PHOBERT_VERSION)
model = PhoBertModel(PHOBERT_VERSION).to(device)
# model.load_state_dict(torch.load(PATH_WEIGHT))


INPUT_QUEUE = "Tác dụng vitamin E?"
questions = pd.read_csv("./data/processed/questions.csv")
number_of_questions = len(questions)
questions["input_queue"] = [INPUT_QUEUE] * number_of_questions

predictions = torch.empty(0).to(device, dtype=torch.float)

test_dataset = PhoBertDataset(
    first_questions = questions['input_queue'].values,
    second_questions = questions['questions'].values,
    targets = None,
    tokenizer = tokenizer
)

test_data_loader = torch.utils.data.DataLoader(
    test_dataset,
    batch_size = 512
)

with torch.no_grad():
    model.eval()
    for batch in tqdm.tqdm(test_data_loader):
        ids = batch["ids"]
        mask = batch["mask"]
        token_type_ids = batch["token_type_ids"]

        ids = ids.to(device, dtype=torch.long)
        mask = mask.to(device, dtype=torch.long)
        token_type_ids = token_type_ids.to(device, dtype=torch.long)

        outputs = model(ids=ids, mask=mask, token_type_ids=token_type_ids)
        predictions = torch.cat((predictions, nn.Sigmoid()(outputs)))
    
    predictions = predictions.cpu().numpy().squeeze()

    questions["label"] = predictions

questions = questions.sort_values(by=['label'], ascending=True)
questions.to_csv("./src/phobert/result.csv", index=False)
