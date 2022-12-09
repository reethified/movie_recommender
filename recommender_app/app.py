from flask import request, Flask, render_template

from .RecommenderService import *

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/recommend1M1' , methods=['POST'])
def recommend1M1():
   return recommender1M1(request.data)

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