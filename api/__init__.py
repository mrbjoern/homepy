import os
import logging

from flask import Flask
from flask_cors import CORS

from api import api


log = logging.getLogger(__name__)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.register_blueprint(api.bp)

    CORS(app)
    return app
