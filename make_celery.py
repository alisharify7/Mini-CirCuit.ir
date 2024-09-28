from Core import create_app
from Config import Setting

flask_app = create_app(Setting)
celery_app = flask_app.extensions["celery"]

