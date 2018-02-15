import sys
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars
#import pymongo

app = Flask(__name__)

mongo = PyMongo(app)
#conn = 'mongodb://localhost:27017'
#client = pymongo.MongoClient(conn)
#db = client.scrape_dict
#mars_collection = db.mars_collection

def print_flush(s):
    print(s)
    sys.stdout.flush()

       
@app.route('/')
def index():
   print_flush("/ requested")
   mars = mongo.db.scrape_dict.find_one()
   return render_template('index.html', scrape_dict=scrape_dict)

@app.route('/test')
def test():
   print_flush("/test requested")
   return 'test'


@app.route('/scrape')
def scrape():
   print_flush("/scrape requested")
   mars = mongo.db.scrape_dict
   mars_data = scrape_mars.scrape()
   mars.update(
       {},
       mars_data,
       upsert=True
   )
   return 'Scraping Successful!'   


if __name__ == "__main__":
    app.run(debug=False)
