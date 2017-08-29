from flask import Flask, redirect, render_template, request, url_for

import os
import sys
import helpers
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name, 100)
    
    total = len(tweets)
    analyzer = Analyzer(os.path.join(sys.path[0], "positive-words.txt"), os.path.join(sys.path[0], "negative-words.txt"))
    positives, negatives, neutrals = 0, 0, 0

    if(total > 0):
        for tweet in tweets:
            score = analyzer.analyze(tweet)
            if score > 0:
                positives += 1
            elif score < 0:
                negatives += 1
            else:
                neutrals += 1
        positive, negative, neutral = positives / total, negatives / total, neutrals / total
    else:
        positive, negative, neutral = 0, 0, 0

    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
