from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping


# Using Flask to: 1) render a template, 2) redirect to another url, and 3) create a URL
app = Flask(__name__)

#  Connect to Mongo using PyMongo
# Use flask_pymongo to set up mongo connection to the URI (uniform resource identifier)
# "app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app"
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Set up our Flask routes

# Flask Main/Home Page Route
@app.route("/")

def index():
   # Use PyMongo to find the "mars" collection in our database
   mars = mongo.db.mars.find_one()
   # Return HTML template using index.html and mars as collection in MongoDB
   return render_template("index.html", mars=mars)

# Flask Scraping Data Route
@app.route("/scrape")

def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, mars_data, upsert=True)
   return redirect('/', code=302)

# Run app.py
if __name__ == "__main__":
       app.run()


# Hey, you know how yesterday they told me to use “insert_one” instead of “update” on the app.py file? 
# Don't do that :joy: instead use the following : mars.update_one({}, {“$set” : mars_data}, upsert=True)
    