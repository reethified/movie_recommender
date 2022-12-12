# The MOVIE RECOMMENDATION PROJECT
## PSL-542

[🔴**Live Recommendation App**](http://rahul86s.pythonanywhere.com/)

[Implementation Notebook](https://github.com/reethified/movie_recommender/blob/master/movie_recommen.ipynb)

## Commands to setup app

    git clone https://github.com/reethified/movie_recommender.git
    cd movie_recommender
    python3 -m venv venv
    source venv/bin/activate
    source .env
    pip install -e '.'
    flask routes
    flask run


## Docker exec commands

    docker image build -t movie_recommender_psl .
    docker run -p 5000:5000 -d movie_recommender_psl
    
    #Push to docker hub
    docker push rahul86s/movie_recommender_psl:latest
    #Pull from docker hub
    docker pull rahul86s/movie_recommender_psl:latest

## Refer

- https://github.com/gasevi/pyreclab
- https://github.com/benfred/implicit
- https://medium.com/radon-dev/als-implicit-collaborative-filtering-5ed653ba39fe
