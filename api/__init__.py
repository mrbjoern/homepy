import os
import logging

from flask import Flask, jsonify
from flask_cors import CORS
from marshmallow import ValidationError

from api import hue_api, temperature_api


log = logging.getLogger(__name__)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    @app.errorhandler(404)
    def not_found(error):
        log.info(error)
        response = jsonify({'error': 'Not found'})
        response.status_code = 404

        return response

    @app.errorhandler(ValidationError)
    def validation_error(error):
        response = jsonify(error.messages)
        response.status_code = 422
        return response

    app.register_blueprint(hue_api.bp)
    app.register_blueprint(temperature_api.bp)

    CORS(app)
    return app
