from flask import request, Flask, render_template, flash

from recommender_app import RecommenderService
from .RecommenderService import *
import numpy as np

app = Flask(__name__)
app.secret_key = "test123"


@app.route('/')
def home():
    return renderIndex()
    #stats = RecommenderService.getStats()
    #generes = stats["generes"]
    #stats.pop("generes")
    #render_template('index.html', stats=stats, generes=generes, selected_genre="None")


@app.route('/recommend1M1', methods=['POST'])
def recommend1M1():
    genre = fetchGenre()
    movies = RecommenderService.recommender1M1(genre)
    return renderIndex(movies=movies,step1=True)


@app.route('/recommender2', methods=['POST'])
def recommender2():
    form = request.form
    selected_movies = {}
    for element in form:
        if element.startswith("rate_"):
            movie = form[element]
            m_split = movie.split("_")
            selected_movies[int(m_split[0])]= int(m_split[1])

    if len(selected_movies) > 1:
        recommendations = RecommenderService.recommender2UBCF(selected_movies)
        return renderIndex(step1=False,step2=True,movies_recommended=recommendations)
    elif len(selected_movies) == 0:
        flash('⚠️ No selection Found! Select your favorites')
        return recommend1M1()
    else:
       return home()


def fetchGenre():
   selected_genre = 'select'
   if 'generes' in request.form:
      selected_genre = request.form['generes']
   elif 'selected_genre' in request.form:
      selected_genre = request.form['selected_genre']
   return selected_genre

def renderIndex(step1=False, step2=False, movies=[],movies_recommended={}):
   selected_genre = fetchGenre()
   stats = RecommenderService.getStats()
   generes = stats["generes"]
   stats.pop("generes")
   return render_template('index.html', selected_genre=selected_genre, stats=stats, generes=generes, step1=step1, step2=step2, movies=movies, movies_recommended=movies_recommended)


if __name__ == '__main__':
    app.debug = True
    app.run()
