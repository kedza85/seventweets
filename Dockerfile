FROM python:3

RUN mkdir -p /usr/src/seventweets
WORKDIR /usr/src/seventweets

COPY requirements.txt /usr/src/seventweets/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/seventweets

ENV GUNICORN_CMD_ARGS="--bind=0:8000 --worker-class=gthread --threads=10"

CMD ["gunicorn", "seventweets:app"]