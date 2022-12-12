from flask import request, Flask, render_template, flash

from recommender_app import RecommenderService

app = Flask(__name__)
app.secret_key = "test123"


@app.route('/')
def home():
    return renderIndex()
    # stats = RecommenderService.getStats()
    # generes = stats["generes"]
    # stats.pop("generes")
    # render_template('index.html', stats=stats, generes=generes, selected_genre="None")


@app.route('/recommend1M1', methods=['POST'])
def recommend1M1():
    genre = fetchGenre()
    movies = RecommenderService.recommender1M1(genre)
    return renderIndex(movies=movies, step1=True)


@app.route('/recommender2', methods=['POST'])
def recommender2():
    form = request.form
    selected_movies = {}
    for element in form:
        if element.startswith("rate_"):
            movie = form[element]
            m_split = movie.split("_")
            selected_movies[int(m_split[0])] = int(m_split[1])

    movies_r1 = RecommenderService.recommender1M1(fetchGenre())

    if len(selected_movies) > 1:
        print(f"Run recommendations using UBCF:{selected_movies}")
        recommendations = RecommenderService.recommender2UBCF(selected_movies)
        return renderIndex(step1=True, step2=True, movies_recommended=recommendations, movies=movies_r1)
    elif len(selected_movies) == 1:
        print(f"Run recommendations using IBCF:{selected_movies}")
        recommendations = RecommenderService.recommender2IBCF(list(selected_movies.keys())[0])
        return renderIndex(step1=True, step2=True, movies_recommended=recommendations, movies=movies_r1)
    else:
        print("No selection found")
        flash('⚠️ No selection Found! Select your favorites')
        return recommend1M1()


def fetchGenre():
    selected_genre = 'select'
    if 'generes' in request.form:
        selected_genre = request.form['generes']
    elif 'selected_genre' in request.form:
        selected_genre = request.form['selected_genre']
    return selected_genre


def renderIndex(step1=False, step2=False, movies=[], movies_recommended={}):
    selected_genre = fetchGenre()
    stats = RecommenderService.getStats()
    generes = stats["generes"]
    stats.pop("generes")
    return render_template('index.html', selected_genre=selected_genre, stats=stats, generes=generes, step1=step1,
                           step2=step2, movies=movies, movies_recommended=movies_recommended)


if __name__ == '__main__':
    app.debug = True
    app.run()
