# import necessary libraries
from flask_sqlalchemy import SQLAlchemy
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    flash)
from recipe_scrapers import scrape_me
from forms import LoginForm
from config import Config
from flask_login import LoginManager, UserMixin, current_user, login_user
from models import User




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
app.config.from_object(Config)
login = LoginManager(app)


#################################################
# Database Setup
#################################################

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"
# # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('postgres://havcrucfklhxkb:81370c5c689e86df56f2ae1b69976b8530fda076d0c74d2b56e34dd7eb253e64@ec2-107-22-160-185.compute-1.amazonaws.com:5432/dflusf4tu5bpr5', '')
db = SQLAlchemy(app)

from .models import User

# Home Page
@app.route("/")
def home():
    user = {'username': 'Will'}
    return render_template('index.html', title='Home', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('login')
        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('login.html', title='Sign In', form=form)


# Save Recipe Button Route
@app.route("/save")
def save():
    user = {'username': 'Will'}
    return render_template('render_recipe.html', title='Home', user=user)

# My Recipes Homepage
@app.route("/myrecipes")
def my_recipes():
    user = {'username': 'Will'}
    recipes = ['chicken parm','waffles','ramen noodles']
    return render_template('myrecipes.html', title='Home', user=user, recipes=recipes)

@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        name = request.form["urlName"]
        data = get_recipes(name)
        # print(data)
        return render_template("render_recipe.html",data=data)
    return render_template("index.html")



if __name__ == "__main__":
    app.run()

