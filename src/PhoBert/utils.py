from PhoBertDataset import PhoBertDataset
import torch
import torch.nn as nn


def loss_fn(outputs, targets):
    # Loss function = binary cross entropy loss
    # using sigmoid to put probabilities in [0,1] interval
    # outputs = torch.squeeze(outputs)
    outputs = outputs.view(-1)
    return nn.BCELoss()(nn.Sigmoid()(outputs), targets)


def get_data_loader(df, targets, batch_size, shuffle, tokenizer, config):
    dataset = PhoBertDataset(
        first_questions=df["question1"].values,
        second_questions=df["question2"].values,
        targets=targets,
        tokenizer=tokenizer,
        config=config
    )

    data_loader = torch.utils.data.DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle
    )
    return data_loader


def phobert_get_train_val_loaders(train_df, val_df, tokenizer, config):
    train_data_loader = get_data_loader(
        df=train_df,
        targets=train_df["label"].values,
        batch_size=config['BATCH_SIZE'],
        shuffle=True,
        tokenizer=tokenizer,
        config=config
    )

    val_data_loader = get_data_loader(
        df=val_df,
        targets=val_df["label"].values,
        batch_size=4*config['BATCH_SIZE'],
        shuffle=True,
        tokenizer=tokenizer,
        config=config
    )

    dataloader_dict = {"train": train_data_loader, "val": val_data_loader}
    return dataloader_dict


def save_checkpoint(save_path, model, optimizer, valid_acc):
    if save_path == None:
        return
    
    state_dict = {'model_state_dict': model.state_dict(),
                  'optimizer_state_dict': optimizer.state_dict(),
                  'valid_acc': valid_acc}

    torch.save(state_dict, save_path)
    print(f'Model saved to ==> {save_path}')


def binary_accuracy(preds, y):
    """
    Returns accuracy per batch, i.e. if you get 8/10 right, this returns 0.8, NOT 8
    """

    # round predictions to the closest integer
    rounded_preds = torch.round(torch.sigmoid(preds))
    correct = (rounded_preds == y).float()  # convert into float for division
    acc = correct.sum() / len(correct)
    return acc

def save_metric(save_path, train_loss_list, val_loss_list, train_acc_list, valid_acc_list, best_valid_acc):
    if save_path == None:
        return
    state_dict = {'train_loss_list': train_loss_list,
                  'val_loss_list': val_loss_list,
                  'train_acc_list': train_acc_list,
                  'valid_acc_list': valid_acc_list,
                  'best_valid_acc': best_valid_acc}
    torch.save(state_dict, save_path)
    print(f'Metric saved to ==> {save_path}')

def load_checkpoint(load_path, model, optimizer):
    if load_path == None:
        return
    state_dict = torch.load(load_path)
    print(f'Model loaded from <== {load_path}')
    model.load_state_dict(state_dict['model_state_dict'])
    optimizer.load_state_dict(state_dict['optimizer_state_dict'])

    return state_dict['valid_acc']

def load_metric(load_path):
    if load_path == None:
        return
    state_dict = torch.load(load_path)
    print(f'Metric load from <== {load_path}')
    return state_dict
