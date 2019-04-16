# Import Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrapeMars
import os


# Hidden authetication file
#import config

# Create an instance of Flask app
app = Flask(__name__)

#Use flask_pymongo to set up connection through mLab
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars_info = mongo.db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_info)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape():

    # Run scrapped functions
    mars_info = mongo.db.mars_info
    mars_data = scrapeMars.scrapeMars_news()
    mars_data = scrapeMars.scrapeMars_image()
    mars_data = scrapeMars.scrapeMars_facts()
    mars_data = scrapeMars.scrapeMars_weather()
    mars_data = scrapeMars.scrapeMars_hemispheres()
    mars_info.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug= True)