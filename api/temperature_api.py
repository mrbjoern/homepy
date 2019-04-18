import logging

from flask import jsonify, request, Blueprint
from marshmallow import Schema, fields, ValidationError, validate

log = logging.getLogger(__name__)

bp = Blueprint('temperature_api', __name__, url_prefix="/temperature")


class TemperatureReading(Schema):
    temperature = fields.Decimal()


@bp.route('/', methods=['GET'])
def get_temperatures():
    return jsonify([{'temperature': 24.0, 'timestamp': 12345}])


@bp.route('/', methods=['POST'])
def add_temperature_reading():
    reading = TemperatureReading().load(request.get_json())
    log.info(reading)
    return jsonify(reading)
