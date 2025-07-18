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

              # 1. Check for NVIDIA CUDA
          if torch.cuda.is_available():
          # Differentiate between NVIDIA and AMD
               if "NVIDIA" in torch.cuda.get_device_name(0):
                    print("NVIDIA CUDA GPU found.")
                    device =  torch.device("cuda")
               # 2. Check for AMD ROCm
               # PyTorch uses the CUDA interface for ROCm, so we check the device name
               if "AMD" in torch.cuda.get_device_name(0):
                    print("AMD ROCm GPU found.")
                    device =  torch.device("cuda") # ROCm uses the 'cuda' device identifier in PyTorch
               
          # 3. Check for Apple Silicon (M1/M2/M3) MPS
          # Note: torch.backends.mps.is_available() is the correct check for recent PyTorch versions
          if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
               print("Apple Silicon GPU (MPS) found.")
               device = torch.device("mps")

          model.to(device)

          print(f"Model sucessfully loaded on device; {device}")

          return model, tokeniser, device
     except OSError:
          print(f"Model not found at: {model_path}")
          sys.exit()