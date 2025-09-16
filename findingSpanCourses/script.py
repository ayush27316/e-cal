import pandas as pd
import os
import glob
import re

def has_span_course(course_codes):
    """
    Check if any course code in the list contains span course indicators.
    Span courses contain: D1, D2, N1, N2, J1, J2
    """
    span_indicators = ["D1", "D2", "N1", "N2", "J1", "J2"]
    
    for course in course_codes:
        if pd.isna(course) or course == '':
            continue
        course_str = str(course).strip()
        for indicator in span_indicators:
            if indicator in course_str:
                return True
    return False

def process_csv_files(folder_path):
    """
    Process all CSV files in the specified folder and find programs with span courses.
    """
    # Get all CSV files in the folder
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in folder: {folder_path}")
        return
    
    programs_with_span_courses = []
    
    print(f"Processing {len(csv_files)} CSV files...")
    
    for csv_file in csv_files:
        try:
            # Read CSV with flexible columns - let pandas handle variable column counts
            with open(csv_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            print(f"Processing: {os.path.basename(csv_file)}")
            
            # Process each line manually to handle variable columns
            for line_num, line in enumerate(lines, 1):
                try:
                    # Strip whitespace and split by comma
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue
                    
                    # Split the line by comma and clean up each field
                    fields = [field.strip().strip('"') for field in line.split(',')]
                    
                    if len(fields) < 2:  # Need at least program name and one course
                        continue
                    
                    # First field is program title, rest are course codes
                    program_title = fields[0]
                    course_codes = fields[1:]
                    
                    # Check if this program has span courses
                    if has_span_course(course_codes):
                        # Add the entire row to our results
                        programs_with_span_courses.append(fields)
                        print(f"  Found span course in: {program_title}")
                        
                except Exception as line_error:
                    print(f"  Warning: Error processing line {line_num} in {os.path.basename(csv_file)}: {str(line_error)}")
                    continue
        
        except Exception as e:
            print(f"Error processing {csv_file}: {str(e)}")
            continue
    
    return programs_with_span_courses

def save_results(programs_with_span_courses, output_file):
    """
    Save the programs with span courses to a new CSV file.
    """
    if not programs_with_span_courses:
        print("No programs with span courses found.")
        return
    
    # Write to CSV manually to handle variable column counts
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        for program in programs_with_span_courses:
            # Join all fields with commas, quoting fields that contain commas
            formatted_fields = []
            for field in program:
                field_str = str(field)
                if ',' in field_str or '"' in field_str:
                    # Escape quotes and wrap in quotes
                    field_str = '"' + field_str.replace('"', '""') + '"'
                formatted_fields.append(field_str)
            
            csvfile.write(','.join(formatted_fields) + '\n')
    
    print(f"\nResults saved to: {output_file}")
    print(f"Found {len(programs_with_span_courses)} programs with span courses.")

def main():
    """
    Main function to process CSV files and find programs with span courses.
    """
    # Configuration
    folder_path = "./departments"
    
    output_file = input("Enter output filename (default: programs_with_span_courses.csv): ").strip()
    if not output_file:
        output_file = "programs_with_span_courses.csv"
    
    # Validate folder path
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return
    
    # Process CSV files
    programs_with_span_courses = process_csv_files(folder_path)
    
    # Save results
    save_results(programs_with_span_courses, output_file)
    
    # Display some statistics
    if programs_with_span_courses:
        print(f"\nSample programs found:")
        for i, program in enumerate(programs_with_span_courses[:5]):  # Show first 5
            print(f"{i+1}. {program[0]}")
        if len(programs_with_span_courses) > 5:
            print(f"... and {len(programs_with_span_courses) - 5} more")

if __name__ == "__main__":
    main()