import torch
import tqdm
from utils import save_checkpoint, binary_accuracy, save_metric, load_metric

def train(model, data_loaders_dict, optimizer, loss_fn, config, device):
    train_loss_list = []
    val_loss_list = []
    train_acc_list = []
    val_acc_list = []
    best_valid_acc = (-1.0)*float("Inf")

    current_epoch = 0

    if config['LOAD_CHECKPOINT']:
        static_dict = load_metric(config['PATH_METRIC'])
        train_loss_list = static_dict['train_loss_list']
        val_loss_list = static_dict['val_loss_list']
        train_acc_list = static_dict['train_acc_list']
        val_acc_list = static_dict['valid_acc_list']
        best_valid_acc = static_dict['best_valid_acc']
        current_epoch += len(train_loss_list)

    for epoch in range(current_epoch, config['EPOCHS']):
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
            
            print("Epoch {}/{} | {:^5} | Loss: {:.4f} | Acc: {:.2f} ".format(epoch + 1, config['EPOCHS'], phase, epoch_loss, epoch_acc))

            if phase == 'train':
                train_loss_list.append(epoch_loss)
                train_acc_list.append(epoch_acc)
            else:
                val_loss_list.append(epoch_loss)
                val_acc_list.append(epoch_acc)

                if best_valid_acc < epoch_acc:
                    best_valid_acc = epoch_acc
                    save_checkpoint(config['PATH_MODEL'], model, optimizer, best_valid_acc)

    save_metric(config['PATH_METRIC'], train_loss_list, val_loss_list, train_acc_list, val_acc_list, best_valid_acc)


