import torch
import tqdm
import numpy as np


def phobert_train_model(model, data_loaders_dict, num_epochs, optimizer, loss_fn,  filename, device):
    for epoch in range(num_epochs):
        # Mỗi epoch sẽ thực hiện 2 phase
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()
            else:
                model.eval()

            epoch_loss = 0.0

            for batch in tqdm.tqdm(data_loaders_dict[phase]):
                ids = batch["ids"].to(device, dtype=torch.long)
                mask = batch["mask"].to(device, dtype=torch.long)
                token_type_ids = batch["token_type_ids"].to(
                    device, dtype=torch.long)
                targets = batch["targets"].to(device, dtype=torch.float)

                # Reset tích lũy đạo hàm
                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(
                        ids, mask=mask, token_type_ids=token_type_ids)

                    loss_value = loss_fn(outputs, targets)
                    epoch_loss += loss_value.item()

                    # Lan truyền ngược và cập nhật tham số nếu phase train
                    if phase == 'train':
                        loss_value.backward()
                        optimizer.step()

            epoch_loss = epoch_loss / len(data_loaders_dict[phase].dataset)

            print("Epoch {}/{} | {:^5} | Loss: {:.4f}".format(epoch +
                                                             1, num_epochs, phase, epoch_loss))

    torch.save(model.state_dict(), filename)
