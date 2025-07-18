import pandas as pd
import torch
import math

BATCH_SIZE = 64

def predict(model, tokeniser, device, excel_path, sheet_name):
    """
    Runs batch prediction using a transformer model on text data from an Excel sheet.

    Args:
        model: A pre-trained HuggingFace model with classification head.
        tokeniser: Corresponding tokenizer for the model.
        device: torch.device to run the model on (e.g., 'cuda' or 'cpu').
        excel_path (str): Path to the Excel file.
        sheet_name (str): Name of the worksheet containing the "Action" column.

    Returns:
        List of predicted label strings, or prints error if failed.
    """
    try:
        # Load Excel data
        df = pd.read_excel(excel_path, sheet_name=sheet_name)

        if "Action" not in df.columns:
            raise KeyError("'Action' column not found in the Excel sheet")

        # Replace NaNs with empty strings
        df['Action'] = df['Action'].fillna('')
        text_list = df["Action"].tolist()

        model.eval()  # Set model to eval mode

        all_predicted_labels = []
        num_batches = math.ceil(len(text_list) / BATCH_SIZE)
        print(f"Processing {len(text_list)} descriptions in {num_batches} batches of size {BATCH_SIZE}...")

        for i in range(0, len(text_list), BATCH_SIZE):
            batch_texts = text_list[i:i + BATCH_SIZE]

            # Tokenize text batch
            inputs = tokeniser(
                batch_texts,
                padding=True,
                truncation=True,
                return_tensors="pt",
                max_length=128
            )

            # Move inputs to the correct device
            inputs = {key: val.to(device) for key, val in inputs.items()}

            # Predict without computing gradients
            with torch.no_grad():
                outputs = model(**inputs)

            # Get predicted class index for each item
            predictions = torch.argmax(outputs.logits, dim=-1)

            # Convert indices to string labels
            predicted_labels_batch = [model.config.id2label[p.item()] for p in predictions]
            all_predicted_labels.extend(predicted_labels_batch)

            print(f"  Processed batch {i // BATCH_SIZE + 1}/{num_batches}")

        print("Prediction complete.")
        return all_predicted_labels

    except FileNotFoundError:
        print(f"Excel file: '{excel_path}' not found")
    except KeyError:
        print(f"Sheet: '{sheet_name}' not found or 'Action' column missing")
    except Exception as e:
        print(f"Error: {e}")
