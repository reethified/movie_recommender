import warnings, os
import pandas as pd
import numpy as np
from recommender_app import RecommenderImpl
from recommender_app.RecommenderImpl import UBCF, IBCF

ubcf = UBCF()
IBCF = IBCF()

def getStats():
    return RecommenderImpl.getIntialVals()

def recommender1M1(genre):
    recommended = RecommenderImpl.genre_recommended[genre]
    result = recommended.index.get_level_values(level=0)
    return result.values.tolist()


def recommender1M2(query):
    queryStr = str(query, 'utf-8')
    print("Search Query:", queryStr)
    return RecommenderImpl.movies.head(5)

def recommender2UBCF(selected_movies):
    """
    Recommender System 2. User Based collaborative filtering
    :param query:
    :return:
    """
    movie_len = ubcf.dataset_shape[1]
    movies = np.zeros(movie_len)
    for movie in selected_movies:
        movies[movie - 1] = selected_movies[movie]
    df=pd.DataFrame(data=movies,index=np.arange(1,movie_len+1)).T
    recommendations = ubcf.recommend(df,n_recommendations=10)
    top_10=recommendations.index.values[0:10]
    ratings = RecommenderImpl.getRating(top_10)
    return {"movies":top_10,"ratings": ratings}


def recommender2IBCF(query):
    """
    Recommender System 2. User Based collaborative filtering
    :param query:
    :return:
    """
    queryStr = str(query, 'utf-8')
    print("Search Query:", queryStr)
    return RecommenderImpl.movies.head(5)