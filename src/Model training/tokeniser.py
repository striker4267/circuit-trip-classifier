from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from utils import CircuitDataset

def tokenise(train_df, val_df, test_df, MODEL_NAME):
    # Load the tokenizer from the specified pre-trained model
    tokeniser = AutoTokenizer.from_pretrained(MODEL_NAME)

    # Tokenize the 'Action' column from each dataframe
    # - truncation: cuts text to max_length
    # - padding: pads shorter sequences to max_length
    # - max_length: sets the maximum length of tokens per example
    train_encodings = tokeniser(train_df['Action'].tolist(), truncation=True, padding=True, max_length=128)
    val_encodings = tokeniser(val_df['Action'].tolist(), truncation=True, padding=True, max_length=128)
    test_encodings = tokeniser(test_df['Action'].tolist(), truncation=True, padding=True, max_length=128)

    print("Tokenisation complete")

    # Wrap tokenised inputs and labels into custom Dataset objects
    train_dataset = CircuitDataset(train_encodings, train_df["Labels"].tolist())
    val_dataset = CircuitDataset(val_encodings, val_df["Labels"].tolist())
    test_dataset = CircuitDataset(test_encodings, test_df["Labels"].tolist())

    print("Datasets created")

    # Return the dataset objects for use in training and evaluation
    return train_dataset, val_dataset, test_dataset, tokeniser
