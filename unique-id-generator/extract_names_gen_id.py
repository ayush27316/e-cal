import pandas as pd

def process_names(input_file, output_excel):
    """
    Processes names from an input file to extract first and last names,
    and generates an ID based on these names. Writes the results to an Excel file.

    Parameters:
    - input_file: Path to the input text file containing names.
    - output_excel: Path to the output Excel file.
    """
    # Define a list of common honorifics (case-insensitive)
    honorifics = {"mr", "mrs", "ms", "dr", "sir", "sr", "jr", "madam", "miss"}

    # Open and read the file
    with open(input_file, "r") as f:
        names = f.readlines()

    processed_data = []

    for name in names:
        name = name.strip()  # Remove any leading/trailing spaces or newlines

        # Split the name into words
        words = name.split()

        if len(words) < 2:
            # If the name has less than 2 words, skip it (invalid name)
            continue

        # Check if the last word is an honorific, ignoring case
        if words[-1].lower().rstrip(".") in honorifics:
            # If the last word is an honorific, treat the second-to-last word as the last name
            last_name = words[-2]
        else:
            # Otherwise, treat the last word as the last name
            last_name = words[-1]

        # Extract the first name
        first_name = words[0]

        # Generate the ID
        unique_id = first_name[0].upper() + last_name.capitalize()

        # Append the processed data to the list
        processed_data.append([first_name, last_name, unique_id])

    # Create a pandas DataFrame with the processed data
    df = pd.DataFrame(processed_data, columns=["First Name", "Last Name", "ID"])

    # Write the DataFrame to an Excel file
    df.to_excel(output_excel, index=False)
    print(f"Processed data has been written to {output_excel}")

# Example usage
input_file = "unique_names.txt"
output_excel = "processed_names.xlsx"

process_names(input_file, output_excel)
