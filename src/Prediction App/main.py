import load
import predict
import insert 
import argparse

MODEL_PATH = "../final model"


def main():

    # 1. Set up the argument parser
    parser = argparse.ArgumentParser(description="Predict circuit trip causes from an Excel file.")
    parser.add_argument("excel_path", help="Full path to the input Excel file.")
    parser.add_argument("--sheet_name", default="Sheet1", help="Name of the sheet to process (default: Sheet1).")
    
    args = parser.parse_args()

    # 2. Use the arguments instead of hardcoded paths
    model, tokeniser, device = load.load_model(MODEL_PATH)
    predicted_causes = predict.predict(model, tokeniser, device, args.excel_path, args.sheet_name)

    if predicted_causes is not None:
        insert.insert(args.excel_path, args.sheet_name, predicted_causes)

if __name__ == "__main__":
    main()





    