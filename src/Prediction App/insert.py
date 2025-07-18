from openpyxl import load_workbook


def insert(excel_file, sheet_name, predicted_causes):
    wb = load_workbook(excel_file)
    ws = wb[sheet_name]

    for col in ws.iter_cols(1, ws.max_column):
        if col[0]. value == "Cause":
            cause_col_idx = col[0].column
            break
    
    ws.insert_cols(cause_col_idx +1)

    ws.cell(row=1, column= cause_col_idx+ 1).value = "Predicted Cause"

    for i, value in enumerate(predicted_causes, start= 2):
        ws.cell(row=i, column= cause_col_idx + 1).value = value

    wb.save(excel_file)

    print(f"Cause predictions saved to {excel_file}")