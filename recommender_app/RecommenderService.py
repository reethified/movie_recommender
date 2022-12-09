import warnings, os
import pandas as pd
data_path = os.path.join(os.path.dirname(__file__), 'dataset')

with warnings.catch_warnings(record=True):
    movies = pd.read_table(f'{data_path}/movies.dat', sep='::', encoding='iso-8859-1', header=None, names= ['MovieID', 'Title', 'Genres'])

def recommender1M1(query):
    queryStr = str(query, 'utf-8')
    print("Search Query:", queryStr)
    return movies.head(5)


def recommender1M2(query):
    queryStr = str(query, 'utf-8')
    print("Search Query:", queryStr)
    return movies.head(5)

def recommender2UBCF(query):
    """
    Recommender System 2. User Based collaborative filtering
    :param query:
    :return:
    """
    queryStr = str(query, 'utf-8')
    print("Search Query:", queryStr)
    return movies.head(5)


def recommender2IBCF(query):
    """
    Recommender System 2. User Based collaborative filtering
    :param query:
    :return:
    """
    queryStr = str(query, 'utf-8')
    print("Search Query:", queryStr)
    return movies.head(5)


