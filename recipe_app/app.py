# import necessary libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from recipe_scrapers import scrape_me

# give the url as a string, it can be url from any site listed below
def get_recipes(url):

    try:
        scraper = scrape_me(url)
    except KeyError:
        print('Website is not supported')

    data = {}
    data['title'] = scraper.title()
    data['ttime'] = scraper.total_time()
    data['yields'] = scraper.yields()
    data['ingredients'] = scraper.ingredients()
    ins = scraper.instructions()
    data['instructions'] = ins.splitlines()
    try: 
        data['image'] = scraper.image()
    except:
        data['image'] = 'No Image Available'
    return data

    

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

# from flask_sqlalchemy import SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"
# # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('postgres://havcrucfklhxkb:81370c5c689e86df56f2ae1b69976b8530fda076d0c74d2b56e34dd7eb253e64@ec2-107-22-160-185.compute-1.amazonaws.com:5432/dflusf4tu5bpr5', '')
# db = SQLAlchemy(app)

# from .models import Pet


@app.route("/")
def home():
    return render_template("form.html")

@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        name = request.form["urlName"]
        data = get_recipes(name)
        # print(data)
        return render_template("renderlist.html",data=data)
    return render_template("form.html")



if __name__ == "__main__":
    app.run()

