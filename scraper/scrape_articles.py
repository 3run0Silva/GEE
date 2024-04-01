import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import time
from datetime import datetime
import schedule

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
    # driver.get("https://www.geneve.ch/en/agenda")

    # Test URL
    driver.get("https://www.geneve.ch/en/agenda?f%5B0%5D=what%3AClubbing")

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
def event_exists(db, title, date):
   events_ref = db.collection('Events')
   query_ref = events_ref.where('title', '==', title).where('date', '==', date)
   docs = query_ref.stream()
   return any(docs)

# Saving logic    
def save_data(all_data, db):
  for event_data in all_data:
    if not event_exists(db, event_data['title'], event_data['date']):
      db.collection('Events').add(event_data)
    else:
       print(f"Event {event_data['title']} on {event_data['date']} already exists in the database")

def run_scraper():
   main_scrape()
   # Updates once a minute for testing purposes
   schedule.every().minute.do(main_scrape)

if __name__ == '__main__':
  run_scraper()
  while True:
      schedule.run_pending()
      time.sleep(1)
