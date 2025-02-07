import pandas as pd

# Load the source and destination Excel files
source_file = 'processed_names.xlsx'  # Path to your source Excel file
destination_file = '3.xlsx'  # Path to your destination Excel file


# Read the source and destination data
source_data = pd.read_excel(source_file)
destination_data = pd.read_excel(destination_file)

# Specify the starting row (1-indexed) where you want to insert data
start_row = 41  # Adjust this to your desired start row

# Get the columns you want to copy (e.g., the first three columns)
source_columns = source_data.columns[:3]  # Adjust based on your requirement

# Extend the destination DataFrame if necessary
required_rows = start_row - 1 + len(source_data)
if required_rows > len(destination_data):
    # Append empty rows to reach the required size
    additional_rows = required_rows - len(destination_data)
    destination_data = pd.concat([destination_data, pd.DataFrame(index=range(additional_rows))], ignore_index=True)

# Insert the data into the destination DataFrame
for i in range(len(source_data)):
    for j in range(len(source_columns)):
        destination_data.iat[start_row - 1 + i, j] = source_data.iat[i, j]  # -1 because index is zero-based

# Save the updated DataFrame back to the destination Excel file
destination_data.to_excel(destination_file, index=False)

print(f"Data transferred successfully from {source_file} to {destination_file} starting at row {start_row}.")

