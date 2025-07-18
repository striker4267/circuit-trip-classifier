Automated Classification of Network Rail Circuit Trips
Author: Matthew Wilson - Omordia

Date: July 2025 

Status: Model Trained & Evaluated

1. How to Use This Tool
This section provides instructions for setting up the environment and running the prediction application on an Excel file.

1.1. Setup & Installation
This project requires Python 3.9+ and a Conda environment to manage dependencies.

Clone the Repository:

git clone https://github.com/striker4267/circuit-trip-classifier.git
cd circuit-trip-classifier

Install Git LFS:
This project uses Git Large File Storage (LFS) to manage the model file. You must install the Git LFS client to download the model correctly.

Download and install from: git-lfs.github.com

Initialize LFS (only needs to be done once per machine):

git lfs install

Create and Activate Conda Environment:

conda create --name circuit_trips python=3.11
conda activate circuit_trips

Install Dependencies:
Install all required packages using the requirements.txt file.

pip install -r requirements.txt

Note: For the best performance, it is highly recommended to run this on a machine with an NVIDIA GPU. The application will automatically use the GPU if available. If not, it will fall back to using the CPU, which will be significantly slower.

1.2. Running Predictions on an Excel File
The application is designed to read circuit trip descriptions from an Excel file, predict the cause for each one, and write the predictions back into a new column in the same file.

Configure the Input File:

Navigate to the src/Prediction App/ directory.

Open the main.py script in a text editor.

Modify the excel_path and sheet_name variables to point to your target Excel file and the correct sheet.

# In main.py
excel_path = "path/to/your/data.xlsx"
sheet_name = "YourSheetName"

Important: The Excel file must contain a column named "Action" with the text descriptions to be classified.

Run the Application:

From your terminal, make sure you are in the src/Prediction App/ directory.

Execute the main script:

python main.py

Check the Results:

The script will process all the rows and then save the results.

Open your original Excel file. A new column named "Predicted Cause" will have been added next to the original "Cause" column, containing the model's predictions.

2. Project Summary
This project addresses the challenge of manually categorizing free-text descriptions of Network Rail circuit trips. By leveraging Natural Language Processing (NLP), this repository provides a complete pipeline to clean, augment, and classify raw trip data into one of 22 consolidated fault categories.

2.1. Model Performance
The final model, a fine-tuned DistilBERT transformer, achieves approximately 98.5% accuracy on unseen data, demonstrating its high reliability for operational use.

Metric

Score

Test Set Accuracy

98.53%

Test Set F1-Score

98.52%

Test Set Precision

98.53%

Test Set Recall

98.53%

2.2. Key Stages & Methodology
Data Processing: Started with ~16,000 raw records. Implemented scripts to clean text and consolidate sparse fault categories into a robust set of 22 classes.

Data Augmentation: Used a resilient, checkpoint-based back-translation pipeline (English -> French -> English) to synthetically increase training data for minority classes, improving model generalization.

Model: Fine-tuned a distilbert-base-uncased model, chosen for its excellent balance of performance and computational efficiency. The model was trained for 5 epochs, with the best-performing version automatically selected based on validation loss.

2.3. Project Structure
The repository is organized into the following key directories:

├── data/
│   ├── combined_data.csv       # Final augmented dataset for training
│   └── ...                     # Raw and intermediate data files
│
└── src/
    ├── Data cleaning/          # Scripts for initial data cleaning
    ├── Model training/         # Scripts for the complete training pipeline
    └── Prediction App/
        ├── final_model/        # The final, best-performing model
        ├── main.py             # Main script to run the prediction app
        ├── load.py, predict.py, insert.py # App modules
        └── ...
