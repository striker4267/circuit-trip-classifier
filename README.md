
Automated Classification of Network Rail Circuit Trips
Author: Matthew Wilson-Omordia

Date: July 2025
Status: Model Trained & Evaluated

1. How to Use the Prediction Application
This section provides instructions for setting up the environment and running predictions on an Excel file using the final, trained model.

# 🤖 Automated Classification of Network Rail Circuit Trips

**Author:** Matthew Wilson-Omordia
**Date:** July 2025
**Status:** Model Trained & Evaluated

---

## 🚀 1. How to Use the Prediction Application


This section provides instructions for setting up the environment and running predictions on an Excel file using the final, trained model.

### 1.1. Setup & Installation

git clone [repository-url]
cd [repository-name]

> **Note:** This project requires Python 3.9+ and a Conda environment to manage dependencies and ensure reproducibility.


1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/striker4267/circuit-trip-classifier.git
    cd circuit-trip-classifier
    ```

2.  **Install Git LFS:**
    This project uses Git Large File Storage (LFS) to manage the model file. You **must** install the Git LFS client to download the model correctly.
    * Download and install from: [git-lfs.github.com](https://git-lfs.github.com)
    * Initialize LFS (only needs to be done once per machine):
        ```bash
        git lfs install
        ```

3.  **Create and Activate Conda Environment:**
    ```bash
    conda create --name circuit_trips python=3.11
    conda activate circuit_trips
    ```

4.  **Install Dependencies:**
    Install all required packages using the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```
    > **Performance Note:** For the best performance, it is highly recommended to run this on a machine with an NVIDIA GPU. The application will automatically use the GPU if available. If not, it will fall back to using the CPU, which will be significantly slower.

### 1.2. Running Predictions on an Excel File

The application is run from the command line. It reads descriptions from an Excel file, predicts the cause for each one, and saves the results to a **new file** with `_predicted` added to the name.

1.  **Prepare Your Command:**
    * Open your terminal (e.g., Anaconda Prompt).
    * Navigate to the application directory:
        ```bash
        cd "src/Prediction App"
        ```
    * The application is run using the format:
        `python main.py [path_to_your_excel_file]`

2.  **Run the Application:**
    * Execute the command, replacing the placeholder with the actual path to your file. For example:
        ```bash
        python main.py "C:\Users\YourUser\Documents\Trip_Data.xlsx"
        ```
    * If your data is not on "Sheet1", you can specify the sheet name:
        ```bash
        python main.py "C:\Users\YourUser\Documents\Trip_Data.xlsx" --sheet_name "MyDataSheet"
        ```
    * **Important:** The Excel file **must** contain a column named `"Action"` with the text descriptions to be classified.

3.  **Check the Results:**
    * The script will process all the rows and save the results.
    * In the same folder as your original Excel file, you will find a new file named `Trip_Data_predicted.xlsx`. This file contains all the original data plus a new `"Predicted Cause"` column.


1.2. Running Predictions on an Excel File
The application is run from the command line and takes the path to an Excel file as input. It reads the descriptions, predicts the cause for each one, and saves the results to a new file with _predicted added to the name.

Prepare Your Command:

Open your terminal (e.g., Anaconda Prompt).

Navigate to the application directory:

cd "src/Prediction App"

You will run the application using the format:
python main.py [path_to_your_excel_file]

Run the Application:

Execute the command, replacing the placeholder with the actual path to your file. For example:

python main.py "C:\Users\YourUser\Documents\Trip_Data.xlsx"

If your data is not on "Sheet1", you can specify the sheet name:

python main.py "C:\Users\YourUser\Documents\Trip_Data.xlsx" --sheet_name "MyDataSheet"

Important: The Excel file must contain a column named "Action" with the text descriptions to be classified.

Check the Results:

The script will process all the rows and save the results.

In the same folder as your original Excel file, you will find a new file named Trip_Data_predicted.xlsx. This file contains all the original data plus a new "Predicted Cause" column.

2. Project Summary
=======
---

## 📊 2. Project Summary


This project addresses the challenge of manually categorizing free-text descriptions of Network Rail circuit trips. By leveraging Natural Language Processing (NLP), this repository provides a complete pipeline to clean, augment, and classify raw trip data into one of 22 consolidated fault categories.

### 2.1. Model Performance

The final model, a fine-tuned **DistilBERT** transformer, achieves approximately **98.5% accuracy** on unseen data, demonstrating its high reliability for operational use.

| Metric              | Score    |
| ------------------- | -------- |
| **Test Set Accuracy** | `98.53%` |
| **Test Set F1-Score** | `98.52%` |
| **Test Set Precision**| `98.53%` |
| **Test Set Recall** | `98.53%` |

### 2.2. Key Stages & Methodology

* **Data Processing:** Started with ~16,000 raw records. Implemented scripts to clean text and consolidate sparse fault categories into a robust set of 22 classes.
* **Data Augmentation:** Used a resilient, checkpoint-based **back-translation** pipeline (English -> French -> English) to synthetically increase training data for minority classes, improving model generalization.
* **Model:** Fine-tuned a `distilbert-base-uncased` model, chosen for its excellent balance of performance and computational efficiency. The model was trained for 5 epochs, with the best-performing version automatically selected based on validation loss.

### 2.3. Project Structure

The repository is organized into the following key directories:

### 2.3. Project Structure

The repository is organized into the following key directories:

* `.gitattributes` - Configures Git LFS for large file handling.
* `README.md` - This file (project documentation).
* `requirements.txt` - List of Python packages required for the project.
* `data/`
    * `...` (Contains all raw, intermediate, and augmented data files).
* `src/`
    * `Data cleaning/`
        * `...` (Scripts for initial data cleaning and augmentation).
    * `Model training/`
        * `...` (Scripts for the complete model training pipeline).
    * `Prediction App/`
        * `main.py` - The main script to run the prediction application.
        * `load.py` - Handles loading the trained model.
        * `predict.py` - Contains the core prediction logic.
        * `insert.py` - Inserts predictions back into the Excel file.
    * `final_model/`
        * `model.safetensors` - The final, trained model weights.
        * `...` (Other model and tokenizer files like `config.json`, `vocab.txt`, etc.).