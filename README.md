# GEEvents Python Course Project

Introduction:

This application aims to provide users with information about events in Geneva in a simple and intuitive way. Such information is scattered across the web, requiring searches or prior knowledge of the event.

Developer:

About this project:

This project uses an MVC architecture and utilizes the following technologies:

Primary:

Python
Flask
Selenium
Firebase
Secondary:

HTML/CSS
Bootstrap
JavaScript
Dependencies:

Axios: $ npm install axios
Flask-cors: $ pip install -u flask-cors
Firebase-admin: $ pip install –user firebase-admin
The idea of the project is to scrape the web for information about events in Geneva and store them in a NoSQL database (Firebase). Once the data is stored, an API is used to manage communication between the front and back ends. Finally, a simple front end allows users to query the database for event data.

Project Environment:

[Docker?]

API Documentation:

API ENDPOINTS:

GET all events
URL: /events
Method: GET
Parameters: None
Response: List of all events.
Example response: http://127.0.0.1:5000/events
GET events by tag
URL: /events/tag/
Method: GET
Parameters:
tag (required): The tag of events to filter.
Response: List of events filtered by tag.
Example response: http://127.0.0.1:5000/events/tag/Dance
GET events by date
URL: /events/date?day=&month=&year=
Method: GET
Parameters:
day, month, year (required): The date to filter.
Response: List of events filtered by day, month, or year.
Example response: http://127.0.0.1:5000/events/date?day=18&month=04&year=2024
Error Handling:

Common error codes:

404 (Not found)
Frontend:

Since the focus of the Python project is mainly on the backend, I've created a frontend using vanilla JavaScript along with HTML and basic CSS/Bootstrap for this initial phase of the project. This allows us to test our API without the need for additional tools.
