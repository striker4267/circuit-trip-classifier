import pandas as pd
from excel import extract_column_to_csv, insert_column_to_excel, insert_combined_to_excel
from cleaner import clean_csv
from translator import translate


excel_file = "data/Trip Data for Matthew.xlsx"
sheet_name = "Sheet1"
column_name = ["Cause","Action"]
combined_data = "data/combined_data.csv"


def main (excel_file, sheet_name, column_name):
    """Cleans the data of the excel file """

    #TODO: Load the column into a CSV File
    
    extract_column_to_csv(excel_file, sheet_name, column_name)
    
    #TODO: Get rid of the whitespace and make the first letter of each word capital 
    [cleaned_csv, rows_to_drop] = clean_csv("data/Trip_Causes_Uncleaned.csv", "data/Action_data.csv")

    translate(cleaned_csv, "data/Action_data.csv", "data/Cause_types.csv", combined_data)

    #TODO: save back into the excel file to visulaise the data
    insert_column_to_excel(cleaned_csv,excel_file, rows_to_drop)
    insert_combined_to_excel(combined_data,excel_file)
    
if __name__ == "__main__":
    main (excel_file, sheet_name, column_name)