from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping


# using Flask to: 1) render a template, 2) redirect to another url, and 3) create a URL
app = Flask(__name__)

# connect to Mongo using PyMongo
# use flask_pymongo to set up mongo connection to the URI (uniform resource identifier)
# app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app"
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Set up our Flask routes:

# main/home page route
@app.route("/")

def index():
   # use PyMongo to find the "mars" collection in our database
   mars = mongo.db.mars.find_one()
   # return HTML template using index.html and mars as collection in MongoDB
   return render_template("index.html", mars=mars)

# flask scraping data route
@app.route("/scrape")

def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   #mars.update_one({}, mars_data, upsert=True)
   mars.update_one({}, {"$set" : mars_data}, upsert=True)
   return redirect('/', code=302)

# run app.py
if __name__ == "__main__":
       app.run()