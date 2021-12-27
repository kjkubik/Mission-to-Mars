# Mission-to-Mars
Web Scraping using BeautifulSoup, Splinter, MongoDB, Flask, HTML, CSS, ChromeDriverManager, Chrome Developer Tools, Python

## Purpose
In this module we create an automated web scrapping app using various tools to scrap the data from several Mars websites, store the data in MongoDB, and display the data as a web page.

The first thing accomplished was creating the script used to do scrapping. These can be found in scraping.py. The main steps for doing so are:

- created an instance of a Splinter browser
- created a function for each website needing scraped by:
  - naming the url of each site being to scrape with splinter
  - converting the browser html to a soup object using Beautiful Soup
  - naming the navigation needing to be followed to capture data needing to scrape
  - moving the data into a list of dictionaries (so that they can be stored)
  - storing and updating database with data scraped from websites
- created the script used for automating the scraping process using Flask. This script can be found in app.py.

The next thing we needed to work with was MongoDB to validate our database collection. MongoDB Compass was used to accomplish this.
![](images/MarsMongoDB.png)

Lastly, we created HTML using Bootstrap and our MongoDB mars collection to accomplish the templates/index.html.
![](images/CompleteWebPage.png) 
