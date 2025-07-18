import load
import predict
import insert 

MODEL_PATH = "results/final model"


def main():

    #excel_path = input("Full path to excel file: ")
    excel_path = "data/Trip Data for Matthew.xlsx"
    #sheet_name = input("Sheet name: ")
    sheet_name = "Sheet1"

    model, tokeniser, device = load.load_model(MODEL_PATH)

    predicted_causes = predict.predict (model, tokeniser, device, excel_path, sheet_name)

    insert.insert(excel_path, sheet_name, predicted_causes)

if __name__ == "__main__":
    main()





    