FROM python:3.8-slim


WORKDIR /usr/src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app app

ENV FLASK_APP="app"
ENV GUNICORN_CMD_ARGS="--workers 4 --worker-class 'gthread' --threads 2"
ENV FLASK_ENV="production"
ENV SERVER_PORT=$PORT
ENV CLIENT_ORIGIN_URL="http://localhost:4200"
ENV AUTH0_AUDIENCE="https://rodrigo-possa-api-todo.herokuapp.com"
ENV AUTH0_DOMAIN="rmpossatodolist.us.auth0.com"


CMD gunicorn -b 0.0.0.0:$PORT "app:create_app()" --log-file=-