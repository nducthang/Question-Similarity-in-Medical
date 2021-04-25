from PhoBertDataset import PhoBertDataset
import torch
from config import BATCH_SIZE
import torch.nn as nn

def loss_fn(outputs, targets):
    # Loss function = binary cross entropy loss
    # using sigmoid to put probabilities in [0,1] interval
    outputs = torch.squeeze(outputs)
    return nn.BCELoss()(nn.Sigmoid()(outputs), targets)

def get_data_loader(df, targets, batch_size, shuffle, tokenizer):
    dataset = PhoBertDataset(
        first_questions=df["question1"].values,
        second_questions=df["question2"].values,
        targets=targets,
        tokenizer=tokenizer
    )

    data_loader = torch.utils.data.DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle
    )
    return data_loader


def phobert_get_train_val_loaders(train_df, val_df, tokenizer):
    train_data_loader = get_data_loader(
        df=train_df,
        targets=train_df["label"].values,
        batch_size=BATCH_SIZE,
        shuffle=True,
        tokenizer=tokenizer
    )

    val_data_loader = get_data_loader(
        df=val_df,
        targets=val_df["label"].values,
        batch_size=4*BATCH_SIZE,
        shuffle=True,
        tokenizer=tokenizer
    )

    dataloader_dict = {"train": train_data_loader, "val": val_data_loader}
    return dataloader_dict
