from flask import Flask, render_template
from routing import nav_entry
from special_sites import errors, bots
import os

app = Flask(__name__)

# Get the path to the website directory
website_dir = os.path.dirname(os.path.abspath(__file__))

# Register routes and error pages
nav_entry(app, website_dir)
errors(app)
bots(app, website_dir)

# Define routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/downloads")
def downloads():
    return render_template("downloads.html")

if __name__ == "__main__":
    app.run(debug=True)