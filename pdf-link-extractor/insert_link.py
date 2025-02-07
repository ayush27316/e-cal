import pandas as pd
excel_file_path = 'Summer2024-course_sections_offered_Ayush.xlsx'
df = pd.read_excel(excel_file_path)
df['LINK'] = 'https://www.mcgill.ca/study/2023-2024/courses/' + df['SUBJECT_CODE'] + '-' + df['COURSE_NUMBER']
df.to_excel(excel_file_path, index=False)