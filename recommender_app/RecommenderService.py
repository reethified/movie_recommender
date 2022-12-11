import warnings, os
import pandas as pd

from recommender_app import RecommenderImpl
from recommender_app.RecommenderImpl import UBCF, IBCF

ubcf = UBCF()
IBCF = IBCF()

def getStats():
    return RecommenderImpl.getIntialVals()

def recommender1M1(query):
    queryStr = str(query, 'utf-8')
    print("Search Query:", queryStr)
    return RecommenderImpl.movies.head(5)


def recommender1M2(query):
    queryStr = str(query, 'utf-8')
    print("Search Query:", queryStr)
    return RecommenderImpl.movies.head(5)

def recommender2UBCF(query):
    """
    Recommender System 2. User Based collaborative filtering
    :param query:
    :return:
    """
    queryStr = str(query, 'utf-8')
    print("Search Query:", queryStr)
    return RecommenderImpl.movies.head(5)


def recommender2IBCF(query):
    """
    Recommender System 2. User Based collaborative filtering
    :param query:
    :return:
    """
    queryStr = str(query, 'utf-8')
    print("Search Query:", queryStr)
    return RecommenderImpl.movies.head(5)