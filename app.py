from flask import Flask, render_template, redirect
import scrape_mars
from flask_pymongo import PyMongo
import pymongo



# conn='mongodb:localhost:27017'
# client=pymongo.MongoClient(conn)
# db = client.planetdb
# collection=db.mars

app=Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")
@app.route("/")
def index():
    data=mongo.db.mars.find_one()
    return render_template("index.html",data=data)

@app.route("/hemispheres")
def hemi():
    data=mongo.db.mars.find_one()
    return render_template("hemi.html", data=data)

@app.route("/scrape")
def scraper():
    mars_data=scrape_mars.scrape()
    mongo.db.mars.update({},mars_data, upsert=True)
    return redirect("/",code=302)


if __name__ == "__main__":
    app.run(debug=True)