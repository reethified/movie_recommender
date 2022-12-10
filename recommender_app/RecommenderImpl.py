import pandas as pd
import warnings, re, os
import seaborn as sns
sns.set_theme()
from sklearn.preprocessing import minmax_scale
import scipy.sparse as sparse
from sklearn.neighbors import NearestNeighbors

data_path = os.path.join(os.path.dirname(__file__), 'dataset')

with warnings.catch_warnings(record=True):
    movies = pd.read_table(f'{data_path}/movies.dat', sep='::', encoding='iso-8859-1', header=None, names= ['MovieID', 'Title', 'Genres'])
    ratings = pd.read_table(f'{data_path}/ratings.dat', sep='::', encoding='iso-8859-1',header=None, names= ["UserID","MovieID","Rating","Timestamp"])
    users = pd.read_table(f'{data_path}/users.dat', sep='::', encoding='iso-8859-1',header=None, names=["UserID","Gender","Age","Occupation","Zip"])

def title_production_yr_split(title):
    groups=re.search('^(.+)\((\d+)\)$',title)
    movie_title=groups.group(1).strip()
    production_year=int(groups.group(2))
    return {"Title_1":movie_title, "Production_Year":production_year}
applied_df = movies.apply(lambda row: title_production_yr_split(row.Title), axis='columns', result_type='expand')
movies = pd.concat([movies, applied_df], axis='columns')
movies["Decade"] =movies.Production_Year//10*10

dummies_genres = movies['Genres'].str.get_dummies()
all_generes=dummies_genres.columns.values.tolist()
movies_cleaned = pd.concat([movies,dummies_genres],axis=1)
movies_cleaned.drop('Genres',inplace=True,axis=1)
total_genres=dummies_genres.columns.values
mov_rat = movies_cleaned.merge(ratings, on='MovieID',how="inner")

def getGenres():
    return all_generes

def getIntialVals():
    return {"users":ratings.UserID.nunique(),"movies":ratings.MovieID.nunique(), 'Ratings': ratings.Rating.unique(), "generes":all_generes}


def recommender1_m1(genre,n=5):
    mov_rat_adv = mov_rat[(mov_rat[genre]==1)]
    mov_rat_adv.reset_index(drop=True,inplace=True)
    genre_grouped= mov_rat_adv[['MovieID','Title_1','Rating']].groupby(['MovieID','Title_1','Rating']).size()
    genre_grouped_df = genre_grouped.to_frame('count').reset_index()
    genre_rating = genre_grouped_df.pivot(index=['MovieID','Title_1'],columns='Rating',values='count').fillna(0)
    genre_rating.columns=['r1','r2','r3','r4','r5']
    def moviescore(r):
        return r.r1*(-1)+r.r2*(-0.5)+r.r3*(-0.1)+r.r4*(0.5)+r.r5
    genre_rating['score']=genre_rating.apply(moviescore,axis=1)
    return genre_rating.score.nlargest(n=n)

def recommender1_m2(genre,n=5,min_count=100):
    mov_rat_adv = mov_rat[(mov_rat[genre]==1)]
    mov_rat_adv.reset_index(drop=True,inplace=True)
    genre_agg= mov_rat_adv[['MovieID','Title_1','Rating']].groupby(['MovieID','Title_1'])['Rating'].agg(Mean='mean', Count='count')
    genre_agg_filtered = genre_agg[genre_agg['Count']>min_count].reset_index()
    genre_agg_filtered.sort_values(by="Mean", ascending=False,inplace=True)
    return genre_agg_filtered.head(n)

class UBCF:
    """
    Recommender 2 Method 1: User Based Collaborative Filtering (UBCF)

    # Recommendation for 501 user
    user=sparse_usr_movie[501,:]
    n_recommendations=20
    mypred=ubcf.recommend(user,n_recommendations)
    mypred.head(100)

    """
    def __init__(self,metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1):
        # Prepare dataset and train model
        self.dataset = mov_rat.pivot_table(index="UserID", columns='MovieID', values="Rating")
        dataset_norm = self.dataset.fillna(0).subtract(self.dataset.mean(axis=1), axis='rows')
        sparse_usr_movie = sparse.csr_matrix(dataset_norm.values)
        ubcf_knn = NearestNeighbors(metric=metric, algorithm=algorithm, n_neighbors=n_neighbors, n_jobs=n_jobs)
        self.ubcf_knn_fit = ubcf_knn.fit(sparse_usr_movie)

    def recommend(self,user, n_recommendations=20):
        distances, indices = self.ubcf_knn_fit.kneighbors(user, n_neighbors=n_recommendations + 1)
        indices = indices.squeeze().tolist()[1:]
        distances = distances.squeeze().tolist()[1:]
        uid_movies = self.dataset.filter(items=indices, axis=0).fillna(0)
        weighted_score = uid_movies.multiply(distances, axis=0).mean(axis=0)
        recommendations = pd.Series(data=minmax_scale(weighted_score, feature_range=(0, 5)), index=uid_movies.columns)
        recommendations.index.name = "MovieID"
        return recommendations.sort_values(ascending=False).astype(int)


class IBCF:
    """
    # Recommend movies based on Item 101
    #movie=sparse_movie_usr[101,:]
    movie=dataset_norm.filter(items=[101],axis=0)
    n_recommendations=20
    recommender2_ibcf(movie,ibcf_knn_fit,n_recommendations)
    """
    def __init__(self,metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1):
        from sklearn.neighbors import NearestNeighbors
        self.dataset = mov_rat.pivot_table(index="MovieID", columns='UserID', values="Rating")
        dataset_norm = self.dataset.fillna(0)
        sparse_movie_usr = sparse.csr_matrix(dataset_norm.values)
        model2_ibcf = NearestNeighbors(metric=metric, algorithm=algorithm, n_neighbors=n_neighbors, n_jobs=n_jobs)
        self.ibcf_knn_fit = model2_ibcf.fit(sparse_movie_usr)

    def recommend(self,movie,n_recommendations=20):
        distances, indices=self.ibcf_knn_fit.kneighbors(movie, n_neighbors=n_recommendations+1)
        indices=indices.squeeze().tolist()[1:]
        distances=distances.squeeze().tolist()[1:]
        recommendations = pd.DataFrame({"Movies":indices,"Score":distances})
        return recommendations.sort_values(by="Score",ascending=False)