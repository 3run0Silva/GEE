import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# Chrome
from webdriver_manager.chrome import ChromeDriverManager

# Firestore
from api.config.database.db import db


# Chromedriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Concerts page URL
# driver.get("https://www.geneve.ch/en/agenda")

# Test URL
driver.get("https://www.geneve.ch/en/agenda?f%5B0%5D=what%3AClubbing")

# Wait time necessary otherwise the description data doesn't appear
wait = WebDriverWait(driver, 10)

# Scraping all articles
articles = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.event")))

def process_articles(articles, all_data):
  for article in articles[:10]:
    event_data = {}

    #Img Scraper
    try:
      img_element = article.find_element(By.CSS_SELECTOR, "img.image")
      img = img_element.get_attribute("src")
    except NoSuchElementException as e:
      print(f"Img: (element not found) {e}")

    # Titles Scraper
    try:
      title_element = article.find_element(By.CSS_SELECTOR, "h3.titre")
      title = title_element.text
    except NoSuchElementException as e:
      print(f"Title: (element not found) {e}")

    # Dates Scraper
    try:
      date_element = article.find_element(By.CSS_SELECTOR, "div.date")
      date = date_element.text
    except NoSuchElementException as e:
      print(f"Date: (element not found) {e}")

    # Descriptions Scraper
    try:
      description_elements = article.find_elements(By.CSS_SELECTOR, "p[class*='text-color-three']")
      description = ' '.join([elem.text for elem in description_elements if elem.text])
    except NoSuchElementException as e:
      print(f"Description: (element not found) {e}")

    # Tags Scraper
    try:
        tag_element = article.find_element(By.CSS_SELECTOR, "p.tags")
        tag = tag_element.text
    except NoSuchElementException as e:
        print(f"Tag: (element not found) {e}")

    print("\n")

    # Fill the dictionary with the data
    
    event_data['img'] = img
    event_data['title'] = title
    event_data['date'] = date
    event_data['description'] = description
    event_data['tag'] = tag
    print(event_data)

    all_data.append(event_data)  

all_data = []

while True:
    
    # Fetch articles for the current page
    articles = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.event")))
    process_articles(articles, all_data)

    # Move to next page
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "a[rel='next']")
        driver.get(next_button.get_attribute('href'))
        time.sleep(2)
    except NoSuchElementException as e:
        print("No more pages to scrape.")
        break 
    
def save_data(all_data):
  for event_data in all_data:
    db.collection('Events').add(event_data)



save_data(all_data)

driver.quit()
