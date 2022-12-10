from flask import request, Flask, render_template

from recommender_app import RecommenderService
from .RecommenderService import *
import numpy as np
app = Flask(__name__)

@app.route('/')
def home():
   stats = RecommenderService.getStats()
   generes = stats["generes"]
   stats.pop("generes")
   return render_template('index.html',stats=stats, generes=generes,selected_genre="None")

@app.route('/recommend1M1' , methods=['POST'])
def recommend1M1():
   selected_genre = request.form['generes']
   movies = (np.arange(6)+1).tolist()
   stats = RecommenderService.getStats()
   generes = stats["generes"]
   stats.pop("generes")
   return render_template('index.html',stats=stats, generes=generes,step1=True, movies=movies,selected_genre=selected_genre)

@app.route('/recommend1M2' , methods=['POST'])
def recommend1M2():
   return recommender1M2(request.data)

@app.route('/recommender2IBCF' , methods=['POST'])
def recommender2M1():
   return recommender2UBCF(request.data)


@app.route('/recommender2UBCF' , methods=['POST'])
def recommender2M2():
   return recommender2IBCF(request.data)

if __name__ == '__main__':
   app.run()