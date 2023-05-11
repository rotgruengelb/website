from flask import Flask, render_template


app = Flask(__name__)
website_dir = (__file__.removesuffix("/__init__.py"))

import routing
import special_sites as specials
routing.nav_entry(app, website_dir); specials.errors(app); specials.bots(app, website_dir)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/downloads")
def downloads():
    return render_template("downloads.html")

if __name__ == '__main__':
    app.run(debug=True)