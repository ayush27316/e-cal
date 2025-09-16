import csv

def find_programs_with_course(filename, course_code):
    programs = []

    with open(filename, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row:
                continue
            program_name = row[0].strip()
            courses = [c.strip() for c in row[1:]]  # all following entries
            if course_code in courses:
                programs.append(program_name)

    return programs


if __name__ == "__main__":
    filename = "programs-with-span-courses.csv"  # replace with your file path
    course_code = input("Enter course code (e.g., COMP 261D1): ").strip()

    results = find_programs_with_course(filename, course_code)

    if results:
        print(f"\nPrograms containing {course_code}:")
        for p in results:
            print(" -", p)
    else:
        print(f"\nNo programs found containing {course_code}.")
