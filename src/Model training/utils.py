import torch 

# Custom Dataset class for use with HuggingFace Transformers and PyTorch
class CircuitDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        # Store tokenized inputs and their corresponding labels
        self.encodings = encodings
        self.labels = labels
    
    def __getitem__(self, index):
        # Retrieve the input tensors at the given index
        item = {key: torch.tensor(val[index]) for key, val in self.encodings.items()}

        # Add the label tensor for this index
        item["labels"] = torch.tensor(self.labels[index])
        return item
    
    def __len__(self):
        # Return the total number of samples
        return len(self.labels)
