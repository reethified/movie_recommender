from flask import request, Flask, render_template, flash

from recommender_app import RecommenderService
from .RecommenderService import *
import numpy as np

app = Flask(__name__)
app.secret_key = "test123"


@app.route('/')
def home():
    stats = RecommenderService.getStats()
    generes = stats["generes"]
    stats.pop("generes")
    return render_template('index.html', stats=stats, generes=generes, selected_genre="None")


@app.route('/recommend1M1', methods=['POST'])
def recommend1M1():
    selected_genre = 'select'
    if 'generes' in request.form:
        selected_genre = request.form['generes']
    elif 'selected_genre' in request.form:
        selected_genre = request.form['selected_genre']

    movies = (np.arange(6) + 1).tolist()
    stats = RecommenderService.getStats()
    generes = stats["generes"]
    stats.pop("generes")
    return render_template('index.html', stats=stats, generes=generes, step1=True, movies=movies,
                           selected_genre=selected_genre)


@app.route('/recommender2', methods=['POST'])
def recommender2():
    form = request.form

    movies = list()
    for element in form:
        if element.startswith("rate_"):
            movies.append(form[element])

    if len(movies) > 0:
        movies = np.zeros(3883)
    else:
        flash('⚠️ No selection Found! Select your favorites')
        return recommend1M1()


if __name__ == '__main__':
    app.debug = True
    app.run()
