import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import sys

def load_model(model_path):
     """
    Loads the fine-tuned model and tokenizer from the specified path.
    Handles moving the model to the GPU if available.
    """
     
     print(f"Loading Model from { model_path}")
     try: 
          tokeniser = AutoTokenizer.from_pretrained(model_path)
          model = AutoModelForSequenceClassification.from_pretrained(model_path)

          device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
          model.to(device)

          print(f"Model sucessfully loaded on device; {device}")

          return model, tokeniser, device
     except OSError:
          print(f"Model not found at: {model_path}")
          sys.exit()