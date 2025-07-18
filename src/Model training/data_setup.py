import pandas as pd
import torch 
from sklearn.model_selection import train_test_split

def prepare(csv_file_path):
    print("Preparing data")

    # Define column names for the CSV since the file has no header row
    column_names = ["Cause", "Action"]

    # Load the CSV into a pandas DataFrame
    df = pd.read_csv(csv_file_path, header=None, names=column_names)
    print(f"Loaded {len(df)} records")

    # Replace missing values in 'Action' column with empty strings
    df['Action'] = df['Action'].fillna('')

    # Label encoding, and get mappings and number of unique labels
    df, label2id, id2label, num_labels = label(df)

    # Split into train, validation, and test sets
    train_df, val_df, test_df = split(df)

    # Return everything needed for model training and evaluation
    return [train_df, val_df, test_df, label2id, id2label, num_labels]

def label(df):
    # Get unique class labels from the 'Cause' column
    unique_cases = df["Cause"].unique().tolist()

    # Create dictionaries to map labels to IDs and vice versa
    label2id = {label: i for i, label in enumerate(unique_cases)}
    id2label = {i: label for i, label in enumerate(unique_cases)}

    # Encode the labels as integers
    df["Labels"] = df["Cause"].map(label2id)

    print("Labels encoded")
    print(f"Mapping: {label2id}")

    return df, label2id, id2label, len(unique_cases)

def split(df):
    # First split: train (80%) and temp (20%)
    train_df, temp_df = train_test_split(
        df,
        test_size=0.2,
        random_state=42,
        stratify=df["Labels"]  # Ensure class balance
    )

    # Second split: validation (10%) and test (10%)
    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.5,
        random_state=42,
        stratify=temp_df["Labels"]
    )

    print(f"Training set size: {len(train_df)}")
    print(f"Validation set size: {len(val_df)}")
    print(f"Test set size: {len(test_df)}")

    return [train_df, val_df, test_df]
