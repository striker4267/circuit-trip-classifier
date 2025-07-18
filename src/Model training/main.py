from data_setup import prepare            # Handles loading, cleaning, labeling, and splitting the data
from tokeniser import tokenise            # Handles tokenizing the text for the model
from train_model import train             # Handles model training and evaluation

def main():
    # Path to the combined CSV file with data
    combined_csv_file_path = "data/combined_data.csv"

    # HuggingFace model name to use for tokenization and classification
    MODEL_NAME = "distilbert-base-uncased"

    # Step 1: Load and prepare the data
    # Returns train/val/test DataFrames, label mappings, and number of unique labels
    train_df, val_df, test_df, label2id, id2label, num_labels = prepare(combined_csv_file_path)

    # Step 2: Tokenize the Action texts in each split using the specified model
    # Returns PyTorch Dataset objects ready for training
    train_dataset, val_dataset, test_dataset, tokeniser = tokenise(train_df, val_df, test_df, MODEL_NAME)

    # Step 3: Train and evaluate the model using the prepared datasets
    train(train_dataset, val_dataset, test_dataset,MODEL_NAME, num_labels, label2id, id2label, tokeniser)

if __name__ == "__main__":
    main()



    
