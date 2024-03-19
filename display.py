from flask import Flask, render_template
import json
from scrape import DPAC_Parser

app = Flask(__name__)

parser = DPAC_Parser()

@app.route("/")
def events():
    with open('db.json', 'r') as db:
        events = json.load(db)
        return render_template('index.html', events=events)

if __name__ == '__main__':
    app.run(debug=True)