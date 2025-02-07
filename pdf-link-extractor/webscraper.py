from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without opening GUI)

# Set up the WebDriver
service = Service("C:\Software\chromedriver\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to check if a URL is valid
def check_url(url):
    driver.get(url)
    if "404" in driver.title:
        print(f"Page not found: {url}")

# Function to find and click on all links on a webpage
def click_links_on_page(url):
    driver.get(url)
    links = driver.find_elements_by_tag_name("a")
    for link in links:
        href = link.get_attribute("href")
        if href:
            check_url(href)

# Example usage
click_links_on_page("https://www.mcgill.ca/study/2024-2025/university_regulations_and_resources/undergraduate/gi_online_distance_programs")

# Close the WebDriver
driver.quit()
