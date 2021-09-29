FROM python:3.8-slim


WORKDIR /usr/src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app app

ENV FLASK_APP="app"
ENV GUNICORN_CMD_ARGS="--workers 4 --worker-class 'gthread' --threads 2"
ENV FLASK_ENV="production"

CMD gunicorn -b 0.0.0.0:$PORT "app:create_app()"