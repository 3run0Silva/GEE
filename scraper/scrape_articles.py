import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import time
from datetime import datetime
import schedule
import hashlib

# Selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chromedriver
from webdriver_manager.chrome import ChromeDriverManager

# Firestore
from api.config.database.db import get_db
from google.cloud.firestore_v1 import SERVER_TIMESTAMP
import warnings
#!!!!!!!!error!!!!!!!!!!
warnings.filterwarnings("ignore", message="Detected filter using positional arguments. Prefer using the 'filter' keyword argument instead.")


# Scraping logic
def main_scrape():
  try:
    db = get_db()

    # Chromedriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Concerts page URL
    driver.get("https://www.geneve.ch/en/agenda")

    # Test URL
    #driver.get("https://www.geneve.ch/en/agenda?f%5B0%5D=what%3AClubbing")

    # Wait time necessary otherwise the description data doesn't appear
    wait = WebDriverWait(driver, 10)

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
        
    save_data(all_data, db)

  except Exception as e:
      print(f"An error occurred: {e}")
  finally:
      if 'service' in locals():
        Service.stop()
      driver.quit()

# Proccessing logic
def process_articles(articles, all_data):
  for article in articles[:10]:
    img = title = description = tag = ''
    

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
      print(f"Raw Date String: {date}")
    except NoSuchElementException as e:
      print(f"Date: (element not found) {e}")
      date = None
    
    if date:
      try:
        date_part = ' '.join(date.split(' ')[1:])
        event_date = datetime.strptime(date_part, "%d %B %Y, %H:%M")

        day = event_date.day
        month = event_date.month
        year = event_date.year
        
        formatted_date_for_storage = event_date.isoformat()
      except ValueError as e:
        print(f"Error parsing date: {e}")
        formatted_date_for_storage = day = month = year = None
    else:
      formatted_date_for_storage = day = month = year = None

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

    # Fill the dictionary with the data only if the data contains a title and date
    if title and date: 
      event_data = {
        'img': img,
        'title': title,
        'date': formatted_date_for_storage,
        'day': day,
        'month': month,
        'year': year,
        'description': description,
        'tag': tag
      }
    
      print(event_data)
      all_data.append(event_data)  

    else:
      print("Some events have incomplete data therefor wont be added to the database")

# Cheking to verify if the document already exists in the DB
def event_exists(db, id):
  events_ref = db.collection('Events')
  query_ref = events_ref.where('id', '==', id)
  docs = query_ref.stream()
  return any(docs)

# Generate hash event ID
def generate_event_id(title, date):
  if date is None:
    return None
  else:
    normalized_data = (title + date).replace(" ", "").lower()
    hasher = hashlib.sha256()
    hasher.update(normalized_data.encode('utf-8'))
    event_id = hasher.hexdigest()
    return event_id

# Saving logic    
def save_data(all_data, db):
  for event_data in all_data:
    event_data['id'] = generate_event_id(event_data['title'], event_data['date'])
    if not event_exists(db, event_data['id']):
      if event_data['date'] is not None:  # Check if date is not None
        if not event_exists(db, event_data['id']):
          # Convert event date to Firestore Timestamp object
          event_date = datetime.strptime(event_data['date'], "%Y-%m-%dT%H:%M:%S")
          event_data['date'] = event_date  # No need to convert to Firestore Timestamp
          db.collection('Events').add(event_data)
        else:
          print(f"Event with the ID of: {event_data['id']} already exists in the database")
      else:
        print("Skipping event with None date.")

def run_scraper():
  main_scrape()
  # Updates once a minute for testing purposes
  schedule.every().week.do(main_scrape)

if __name__ == '__main__':
  run_scraper()
  while True:
      schedule.run_pending()
      time.sleep(1)
