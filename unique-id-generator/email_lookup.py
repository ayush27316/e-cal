import requests
from bs4 import BeautifulSoup
import pandas as pd

def find_email(name):

    search_url = f"https://outlook.office.com/mail/search?q={name.replace(' ', '+')}"
    
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    email_element = soup.select_one('.email-class')  # Update this with actual class or ID
    
    if email_element:
        return email_element.text.strip()
    return None

def add_emails_to_sheet(input_file, output_file):
    data = []

    with open(input_file, "r") as f:
        for line in f:
            name = line.strip()
            if name:
                email = find_email(name)  # Automatically find email
                data.append({"Name": name, "Email": email if email else "Not found"})

    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)

    print(f"Names and emails have been saved to {output_file}")

# Example usage
input_file = "unique_names.txt"
output_file = "names_with_emails.xlsx"

add_emails_to_sheet(input_file, output_file)
