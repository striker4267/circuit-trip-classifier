import pandas as pd
import torch
import math

BATCH_SIZE = 64

def predict(model, tokeniser, device, excel_path, sheet_name):
    try:

        df = pd.read_excel(excel_path,sheet_name= sheet_name )

        if "Action" not in df.columns:
            raise KeyError("'Action' column not found in the Excel sheet")
        
        df['Action'] = df['Action'].fillna('')  # Replace NaN with empty string

        text_list = df["Action"].tolist()

        

            # Ensure the model is in evaluation mode (disables dropout, etc.)
        model.eval()
        
        all_predicted_labels = []
        
        # Calculate the total number of batches
        num_batches = math.ceil(len(text_list) / BATCH_SIZE)
        print(f"Processing {len(text_list)} descriptions in {num_batches} batches of size {BATCH_SIZE}...")

        # Process the data batch by batch
        for i in range(0, len(text_list), BATCH_SIZE):
            # Get the current slice of text from the input list
            batch_texts = text_list[i:i + BATCH_SIZE]
            
            # Tokenize the batch of text
            inputs = tokeniser(
                batch_texts, 
                padding=True, 
                truncation=True, 
                return_tensors="pt", 
                max_length=128
            )
            
            # Move the tokenized inputs to the same device as the model (the GPU)
            inputs = {key: val.to(device) for key, val in inputs.items()}

            # Get model predictions without calculating gradients
            with torch.no_grad():
                outputs = model(**inputs)

            # Find the class with the highest score for each item in the batch
            predictions = torch.argmax(outputs.logits, dim=-1)
            
            # Convert the numerical predictions back to string labels
            predicted_labels_batch = [model.config.id2label[p.item()] for p in predictions]
            
            # Add the results from this batch to our final list
            all_predicted_labels.extend(predicted_labels_batch)
            
            # Optional: Print progress for the user
            print(f"  Processed batch {i//BATCH_SIZE + 1}/{num_batches}")

        print("Prediction complete.")
        return all_predicted_labels
    except FileNotFoundError:
        print(f"Excel file: '{excel_path}' not found")
    except KeyError:
        print (f"Sheet: '{sheet_name}' not found ")
    except Exception as e:
        print(f"Error: {e}")