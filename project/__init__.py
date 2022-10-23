from project.AppManager import AppManager

from flask import Flask

def create_app(test_config=None):
    flask_app = Flask(__name__, instance_relative_config=True)
    app = AppManager(flask_app, test_config)
    return flask_app