import pandas as pd

def load_user_data_from_excel(file_path, sheet_name):
    # Read the specified sheet of the Excel file into a DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Create a dictionary to store user data
    user_data = {}
    
    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        # Use userID as the key and store the other columns as a dictionary
        user_data[row['userID']] = {
            'email': row['User Email Address (Optional, Please review instructions)'],
            'first_name': row['User First Name'],
            'last_name': row['User Last Name']
        }
    
    return user_data

def get_user_data(user_data, user_id):
    # Retrieve user data by userID
    return user_data.get(user_id, "User ID not found.")


user_data = load_user_data_from_excel("sheet.xlsx", "UserIDInfo")
user_id = input("Enter userID to search: ")
print(get_user_data(user_data, user_id))




df = pd.read_excel("sheet.xlsx", sheet_name="RolesData")

# Initialize the data structure
role_data = {}

# Iterate over each row in the dataframe
for _, row in df.iterrows():
    role_name = row['RoleName']  # Assuming the column is named 'RoleName'
    users = row['UserList (single line, comma separated, no blanks)'].split(',')  # Split the user IDs into a list
    email = row['Email (optional, please review instructions)']  # Assuming the column is named 'email address'

    # Store data in the dictionary
    role_data[role_name] = {
        'users': users,
        'email': email
    }

# Example of how to extract data based on RoleName
#role_name_to_query = 'GPS Ag Editor'  # Replace with the desired RoleName
#if role_name_to_query in role_data:
#    print(f"Data for role '{role_name_to_query}':")
#    print(f"Users: {role_data[role_name_to_query]['users']}")
#    print(f"Email: {role_data[role_name_to_query]['email']}")
#else:
    #print(f"Role '{role_name_to_query}' not found.")



file_path = 'areas-study.xlsx'

with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
    # Load the first sheet to get unique RoleNames
    sheet1 = pd.read_excel(file_path, sheet_name='WorkflowData')  # Replace with actual sheet name
    unique_roles = sheet1['Page Owner [initiator] (single line, comma separated, no blanks)'].unique()

    # Prepare data for the second and third sheets
    data_for_sheet2 = []
    data_for_sheet3 = []

    for role in unique_roles:
        if role in role_data:  # Use the dictionary created earlier
            # Prepare data for sheet 2
            user_list = role_data[role]['users']
            user_list_str = ','.join(user_list)
            email = role_data[role]['email']
            data_for_sheet2.append({
                'RoleName': role,
                'Userlist': user_list_str,
                'Email': email
            })

            # Prepare data for sheet 3
            for user_id in user_list:
                if user_id in user_data:  # Ensure user_id exists in user_data
                    user_info = user_data[user_id]
                    data_for_sheet3.append({
                        'userID': user_id,
                        'User Email Address (Optional, Please review instructions)': user_info['email'],
                        'User First Name': user_info['first_name'],
                        'User Last Name': user_info['last_name']
                    })
                else:
                    print(f"Warning: user_id '{user_id}' not found in user_data!")

    # Convert the data into DataFrames
    if data_for_sheet2:
        sheet2_df = pd.DataFrame(data_for_sheet2, columns=['RoleName', 'Userlist', 'Email'])
        sheet2_df.to_excel(writer, sheet_name='RolesData', index=False)
    else:
        print("No data for RolesData sheet!")

    if data_for_sheet3:
        sheet3_df = pd.DataFrame(data_for_sheet3, columns=[
            'userID',
            'User Email Address (Optional, Please review instructions)',
            'User First Name',
            'User Last Name'
        ])
        sheet3_df.to_excel(writer, sheet_name='UserIDInfo', index=False)
    else:
        print("No data for UserIDInfo sheet!")

print("Data has been filled successfully.")






