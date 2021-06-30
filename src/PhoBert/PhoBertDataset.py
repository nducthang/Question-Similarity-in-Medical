import torch

class PhoBertDataset(torch.utils.data.Dataset):
    def __init__(self, first_questions, second_questions, targets, tokenizer, config):
        self.first_questions = first_questions
        self.second_questions = second_questions
        self.targets = targets
        self.tokenizer = tokenizer
        self.length = len(first_questions)
        self.config = config

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        first_questions = str(self.first_questions[index])
        second_questions = str(self.second_questions[index])

        # Remove extra white spaces from questions
        first_questions = " ".join(first_questions.split())
        second_questions = " ".join(second_questions.split())

        inputs = self.tokenizer.encode_plus(
            first_questions,
            second_questions,
            add_special_tokens=True,
            padding='max_length',
            max_length=2 * self.config['MAX_LEN'] + 3,  # max length o 2 questions and 3 spectial tokens
            truncation=True
        )

        # Return targets 0, when using dataset in testing and targets are none
        return {
            "ids": torch.tensor(inputs["input_ids"], dtype=torch.long),
            "mask": torch.tensor(inputs["attention_mask"], dtype=torch.long),
            "token_type_ids": torch.tensor(inputs["token_type_ids"], dtype=torch.long),
            "targets": torch.tensor(int(self.targets[index]), dtype=torch.long) if self.targets is not None else 0
        }
