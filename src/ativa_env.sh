export FLASK_APP=app
export FLASK_ENV=development
export GUNICORN_CMD_ARGS="--workers 4 --worker-class 'gthread' --threads 2"
