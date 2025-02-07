import subprocess
import pandas as pd

excel_file_path = 'table_result_real.xlsx'

# Read the Excel sheet into a DataFrame
df = pd.read_excel(excel_file_path)

# Extract the numbers from a specific column (replace 'column_name' with the actual column name)
column_name = 'Page#'
ls = df[column_name].tolist()

url = "https://www.mcgill.ca/study/2023-2024/files/study.2023-2024/2023-2024_undergraduate_ecalendar_2nd_edition.pdf#page="
index = 0

while (True):
    user_input = input();
    if(user_input == "x"):
        break
    elif(user_input == "n"):       
        subprocess.run(["start", "", url + str(ls[index])], shell=True)
        index+=1
    elif (index == len(ls) -1):
        break
    else:
        continue
    
