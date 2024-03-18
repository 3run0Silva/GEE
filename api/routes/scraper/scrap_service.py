from google.cloud import firestore
from scrap.py import
# Initialize Firestore client
db = firestore.Client()

# Your existing scraping code here

for article in articles:
    # Scraping code remains the same, gather data into a dictionary
    event_data = {
        'title': title,
        'date': date,
        'description': description,
        'tag': tag
    }
    
    # Add a new document to the 'events' collection
    db.collection('events').add(event_data)

# Make sure to close the browser
driver.quit()
