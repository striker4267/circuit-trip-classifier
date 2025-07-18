Automated Classification of Network Rail Circuit Trips
Author: Matthew Wilson-Omordia
Date: July 2025
Status: Model Trained & Evaluated

1. Project Overview
This project addresses the challenge of manually categorizing free-text descriptions of Network Rail circuit trips. By leveraging Natural Language Processing (NLP), this repository provides a complete pipeline to clean, augment, and classify raw trip data into one of 22 consolidated fault categories.

The primary goal is to automate this classification process, saving significant time and improving data consistency. The final model, a fine-tuned DistilBERT transformer, achieves approximately 98.5% accuracy on unseen data, demonstrating its high reliability for operational use.

2. Key Features
Data Cleaning: Scripts to process and clean raw text from ~16,000 initial records.

Category Consolidation: Logic to merge sparse fault categories into a more robust set of 22 classes.

Data Augmentation: A resilient, checkpoint-based back-translation pipeline to synthetically increase training data for minority classes.

Model Training: A complete, end-to-end training script to fine-tune a distilbert-base-uncased model on the prepared dataset.

Prediction: A simple, standalone script to load the final model and classify new, unseen trip descriptions.

3. Model Performance
The final model was trained for 3 epochs and evaluated on a held-out test set. The performance metrics highlight its excellent predictive power and generalization capabilities.

Metric

Score

Test Set Accuracy

98.46%

Test Set F1-Score

98.45%

Test Set Precision

98.46%

Test Set Recall

98.46%

4. Project Structure
The repository is organized into the following key directories:

├── data/
│   ├── combined_data.csv       # Final augmented dataset for training
│   └── ...                     # Raw and intermediate data files
│
├── results/
│   ├── final_model/            # The final, best-performing model
│   └── ...                     # Training checkpoints and logs
│
└── src/
    ├── Data cleaning/          # Scripts for initial data cleaning
    └── Model training/
        ├── main.py             # Main script to run the training pipeline
        ├── data_setup.py       # Data loading and splitting
        ├── tokeniser.py        # Text tokenization logic
        ├── train_model.py      # Model training and evaluation
        └── predict.py          # Script for running predictions

5. Setup & Installation
This project uses a Conda environment to manage dependencies.

Clone the Repository:

git clone [repository-url]
cd [repository-name]

Create and Activate Conda Environment:
It is recommended to create a new environment to avoid package conflicts.

conda create --name circuit_trips python=3.11
conda activate circuit_trips

Install Dependencies:
Install all required packages using the provided requirements.txt file.

pip install -r requirements.txt

Note: This project requires PyTorch with CUDA support to leverage GPU acceleration. Ensure your system has a compatible NVIDIA GPU and drivers.

6. Usage
Training the Model
To run the entire data preparation and training pipeline from scratch, execute the main script from within the src/Model training/ directory:

python main.py

The final model will be saved in the results/ directory.

Running Predictions
To classify new trip descriptions using the trained model:

Navigate to the src/Model training/ directory.

Open the predict.py script and modify the new_trip_descriptions list with your data.

Run the script from the terminal:

python predict.py

The predicted categories will be printed to the console.

7. Methodology
Model: distilbert-base-uncased, a smaller, faster version of BERT, was chosen for its excellent balance of performance and computational efficiency, making it ideal for fine-tuning on an RTX 4050 GPU.

Data Augmentation: Back-translation (English -> French -> English) was used to generate synthetic data for classes with fewer than 300 samples. This technique creates new, grammatically correct sentences that are semantically similar to the originals, helping the model generalize better without overfitting.

8. Future Work
Hyperparameter Tuning: Experiment with different learning rates, batch sizes, and training epochs to potentially improve model performance further.

Class Weighting: Although data augmentation helped, implementing class weights during training could further improve performance on the remaining minority classes.

Deployment: Package the prediction script and model into a simple API (e.g., using Flask or FastAPI) for easier integration into other systems.