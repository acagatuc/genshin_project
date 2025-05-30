from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import json
import os
from dotenv import load_dotenv

# initialize webdriver
cService = webdriver.ChromeService(executable_path='/usr/bin/chromedriver')
driver = webdriver.Chrome(service = cService)

# initialize variables
characters = []
dict_indexes = ["sprite", "name", "quality", "element", "weapon", "region", "gender"]

# load in filename from env file
load_dotenv()
filename = os.getenv("BACKUP_FILE")

# navigate to the page to get character info
driver.get("https://genshin-impact.fandom.com/wiki/Character/List")
wait = WebDriverWait(driver, 20)

# get the table info and rows of the playable characters table
table = driver.find_elements(By.TAG_NAME, "tbody")
rows = table[0].find_elements(By.TAG_NAME, "tr")

# for each character in the table, save details
for i in range(len(rows)):
    # initialize empty character dict
    character = {}

    #get table details per character
    details = rows[i].find_elements(By.TAG_NAME, "td")

    for index, d in enumerate(details):
        if index == 0:
            img = d.find_element(By.XPATH, './/span/a/img').get_attribute("data-src")
            character[dict_indexes[index]] = img
            print(img)
        elif index == 2:
            quality = d.find_element(By.XPATH, './/span/span/img')
            character[dict_indexes[index]] = quality.get_attribute("alt")
        elif index == 6:
            character[dict_indexes[index]] = d.text.split(" ")[1]
        elif index == 7:
            break
        else:
            character[dict_indexes[index]] = d.text
    characters.append(character)

with open(filename, 'w') as file:
    json.dump(characters, file, indent=4) # indent for pretty formatting

driver.quit()