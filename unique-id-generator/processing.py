def remove_duplicates_and_count(input_file, output_file):
    """
    Reads names from the input file, removes any duplicate names,
    and writes only unique names to the output file while printing the count.

    Parameters:
    - input_file: Path to the input text file containing names.
    - output_file: Path to the output text file to save unique names.
    """
    unique_names = set()

    # Open the input file and read each line
    with open(input_file, "r") as f:
        for line in f:
            name = line.strip()  # Remove leading/trailing whitespace

            if name and name not in unique_names:
                # If the name is not empty and not already in the set, add it
                unique_names.add(name)

    # Write the unique names to the output file
    with open(output_file, "w") as f:
        for name in sorted(unique_names):  # Sort alphabetically for neatness
            f.write(name + "\n")

    # Print the count of unique names
    unique_count = len(unique_names)
    print(f"Duplicate names removed. {unique_count} unique names have been written to {output_file}")

# Example usage
input_file = "final_cleaned_names.txt"
output_file = "unique_names.txt"

remove_duplicates_and_count(input_file, output_file)
