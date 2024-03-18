from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup Selenium with ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://www.geneve.ch/en/agenda?f%5B0%5D=what%3AConcert")

# Use WebDriverWait to wait for the element to be present
wait = WebDriverWait(driver, 10)

# Find all the event articles
articles = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.event")))

for article in articles:
    try:
        try:
        # Titles
          title_element = article.find_element(By.CSS_SELECTOR, "h3.titre")
          title = title_element.text
          print(f"Title: {title}")
        except NoSuchElementException:
          print("Title: (element not found)")

        # Dates
        try:
          date_element = article.find_element(By.CSS_SELECTOR, "div.date")
          date = date_element.text
          print(f"Date: {date}")
        except NoSuchElementException:
          print("Date: (element not found)")

        # Descriptions
        description = ""
        # Trying to find the description within the context of the article
        description_elements = article.find_elements(By.CSS_SELECTOR, "p[class*='text-color-three']")
        if description_elements:
            # If there are multiple paragraphs, join their texts.
            description = ' '.join([elem.text for elem in description_elements if elem.text])
        if not description:
            print("Description not found.")
        else:
            print(f"description: {description}")

        
        # Tags
        try:
            tag_element = article.find_element(By.CSS_SELECTOR, "p.tags")
            tag = tag_element.text
            print(f"Tag: {tag}")
        except NoSuchElementException:
            print("Tag: (element not found)")

        print("\n")
    except NoSuchElementException:
        print(f"An element in the article was not found: {e}")

# Make sure to close the browser
driver.quit()
