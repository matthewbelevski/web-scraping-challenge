from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars

# Create an instance of Flask
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")



# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    
    #updates the table with the scraped info from mission_to_mars
    mars = mongo.db.mars
    data = mission_to_mars.scrape_info()
    mars.update({}, data, upsert=True)
    return redirect("/", code=302)



if __name__ == "__main__":
    app.run(debug=True)

