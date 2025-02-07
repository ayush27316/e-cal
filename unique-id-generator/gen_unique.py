import pandas as pd

def extract_unique_names(file_paths, sheet_names, columns_to_read, output_file):
    """
    Extract unique names from specified columns in multiple Excel sheets and write them to a text file.

    Parameters:
    - file_paths: List of paths to Excel files (str).
    - sheet_names: List of sheet names to read from (str).
    - columns_to_read: List of column names or indices to extract names from.
    - output_file: Path to the output text file.
    """
    unique_names = set()

    # Loop over each file
    for file_path in file_paths:
        for sheet in sheet_names:
            try:
                # Read the specified sheet and columns from the Excel file
                data = pd.read_excel(file_path, sheet_name=sheet, usecols=columns_to_read)
                
                # Extract unique names from the specified columns
                for col in columns_to_read:
                    unique_names.update(data[col].dropna().unique())
                    
            except Exception as e:
                print(f"Error reading {sheet} from {file_path}: {e}")
    
    # Write the unique names to the output file
    with open(output_file, "w") as f:
        for name in sorted(unique_names):
            f.write(str(name) + "\n")

    print(f"Unique names have been written to {output_file}")




# Example usage
file_paths = ["1.xlsx", "2.xlsx", "4.xlsx", "5.xlsx", "6.xlsx", "7.xlsx"] # Add your Excel file paths here
#file_paths = ["1.xlsx", "2.xlsx", "3.xlsx", "4.xlsx", "5.xlsx", "6.xlsx", "7.xlsx"]
sheet_names = ["FAES", "Arts", "BSE", "Dent", "Mgmt", "Edu", "Eng", "Law", "Med", "Nurs", "SPOT", "Main", "URR", "BASC", "Science", "Music", "Abroad", "UG URR", "GPS URR", "SCS URR", "HS URR (UG URR applied)"]  # Replace with actual sheet names
columns_to_read = ["EDITOR", "APPROVER", "COORDINATOR", "COORDINATOR 2", "COPY EDITOR", "TECHNICAL VERIFICATION"]  # Replace with column names or indices
output_file = "unique_names.txt"

extract_unique_names(file_paths, sheet_names, columns_to_read, output_file)
