import torch
import tqdm
from utils import save_checkpoint, binary_accuracy, save_metric

def train(model, data_loaders_dict, num_epochs, optimizer, loss_fn, config, device):
    train_loss_list = []
    val_loss_list = []
    train_acc_list = []
    val_acc_list = []
    best_valid_acc = (-1.0)*float("Inf")

    for epoch in range(num_epochs):
        # Mỗi epoch sẽ thực hiện 2 phase
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()
            else:
                model.eval()

            epoch_loss = 0.0
            epoch_acc = 0.0

            for batch in tqdm.tqdm(data_loaders_dict[phase]):
                ids = batch["ids"].to(device, dtype=torch.long)
                mask = batch["mask"].to(device, dtype=torch.long)
                token_type_ids = batch["token_type_ids"].to(device, dtype=torch.long)
                targets = batch["targets"].to(device, dtype=torch.float)

                # Reset tích lũy đạo hàm
                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(ids, mask=mask, token_type_ids=token_type_ids)

                    loss_value = loss_fn(outputs, targets)
                    epoch_loss += loss_value.item()

                    accuracy = binary_accuracy(outputs, targets)
                    epoch_acc += accuracy.item()

                    # Lan truyền ngược và cập nhật tham số nếu phase train
                    if phase == 'train':
                        loss_value.backward()
                        optimizer.step()

            epoch_loss = epoch_loss / len(data_loaders_dict[phase].dataset)
            epoch_acc = epoch_acc / len(data_loaders_dict[phase].dataset)
            
            if phase == 'train':
                train_loss_list.append(epoch_loss)
                train_acc_list.append(epoch_acc)
            else:
                val_loss_list.append(epoch_loss)
                val_acc_list.append(epoch_acc)

                if best_valid_acc > epoch_acc:
                    best_valid_acc = epoch_acc
                    save_checkpoint(config['PATH_MODEL'], model, optimizer, best_valid_acc)

            print("Phase:{:^5} | Epoch {}/{} | {:^5} | Loss: {:.4f} | Acc: {:.2f} ".format(phase, epoch + 1, num_epochs, phase, epoch_loss, epoch_acc))

    save_metric(config['PATH_METRIC'], train_loss_list, val_loss_list, train_acc_list, val_acc_list)


