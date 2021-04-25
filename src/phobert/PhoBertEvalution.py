import torch
import torch.nn as nn
import numpy as np
from config import SEED, PHOBERT_VERSION, PATH_WEIGHT
from PhoBertModel import PhoBertModel
from transformers import AutoTokenizer

def eval(model, tokenizer, first_question, second_question, device):
    inputs = tokenizer.encode_plus(
        first_question,
        second_question,
        add_special_tokens=True,
    )

    ids = torch.tensor([inputs["input_ids"]], dtype=torch.long).to(device, dtype=torch.long)
    mask = torch.tensor([inputs["attention_mask"]], dtype=torch.long).to(device, dtype=torch.long)
    token_type_ids = torch.tensor([inputs["token_type_ids"]], dtype=torch.long).to(device, dtype=torch.long)

    with torch.no_grad():
        model.eval()
        output = model(ids=ids, mask=mask, token_type_ids=token_type_ids)
        prob = nn.Sigmoid()(output).item()

        print("questions [{}] and [{}] are {} with score {}".format(first_question, second_question, 'similar' if prob > 0.5 else 'not similar', prob))

np.random.seed(SEED)
torch.cuda.manual_seed(SEED)
torch.cuda.manual_seed_all(SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = True
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(PHOBERT_VERSION)
model = PhoBertModel(PHOBERT_VERSION).to(device)
# model.load_state_dict(torch.load(PATH_WEIGHT))
first_question = "Tác dụng của vitamin E?"
second_question = "vitamin E có tác dụng gì?"

eval(model, tokenizer, first_question, second_question, device)