# syntax=docker/dockerfile:1

FROM python:3.9-buster

WORKDIR /movie_rec
ADD recommender_app /movie_rec/recommender_app
COPY setup.py .
COPY requirements.txt .
COPY README.md .
COPY .env .
RUN python3 -V
RUN python3 -m venv venv
#RUN source venv/bin/activate
RUN ["/bin/bash", "-c", "source venv/bin/activate"]
ENV FLASK_APP recommender_app/app.py
ENV FLASK_ENV development
ENV FLASK_RUN_HOST localhost
ENV FLASK_RUN_PORT 5000
RUN pip install python-dotenv
RUN pip install -e '.'
RUN flask routes

CMD [ "python3", "-m" , "flask", "run"]