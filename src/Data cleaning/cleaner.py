# Import necessary libraries
import pandas as pd  # Used for data manipulation and analysis
import csv  # Provides functionality for handling CSV files (not used directly here, but imported)

# Define a function to clean the CSV file
def clean_csv(cause_file, action_file):
    try:
        # Read the CSV file into a pandas DataFrame
        df_c = pd.read_csv(cause_file)
        df_a = pd.read_csv(action_file)
        
        nan_rows = df_a.isnull().any(axis=1).values.tolist() # finds all the rows with null
        nff_rows = df_c[df_c.columns[0]].astype(str).str.contains("No fault found", na=False).values.tolist() # finds all the rows that contain "No fault found"

        rows_to_drop = list()

        for row_num in range(len(nan_rows)):
            if nan_rows[row_num] and not nff_rows[row_num]:
                rows_to_drop.append(row_num)

        # Will get rid of the rows that contain both the nan and a cause that is not no fault found            
        df_a = df_a.drop(rows_to_drop)
        df_c = df_c.drop(rows_to_drop)
        # Get the name of the first column
        column_name = df_c.columns[0]

        # Remove leading and trailing whitespace from all values in the first column
        df_c[column_name] = df_c[column_name].astype(str).str.strip()
        
        # Capitalize the first letter of each string in the first column
        df_c[column_name] = df_c[column_name].astype(str).str.lower()

        # Define the output file path for the cleaned data
        output_file_c = "data/Trip_Causes_Cleaned.csv"
        output_file_a = action_file
        
        # Save the cleaned DataFrame and actions to a new CSV file (without the index column)
        df_c.to_csv(output_file_c, index=False)
        df_a.to_csv(output_file_a, index = False)

        # Print confirmation message
        print(f"The cleaned data has been saved to {output_file_c}")
        
        # Return the path to the cleaned file
        return [output_file_c,rows_to_drop]

    except FileNotFoundError:
        # Print an error message if the input CSV file is not found
        print(f"Error: the file {cause_file} has not been found")

# Run the cleaning function if this script is executed directly
if __name__ == "__main__":
    clean_csv("data/Trip_Causes_Uncleaned.csv","data/Action_data.csv" )
