import logging

from flask import Flask, jsonify, request
from marshmallow import Schema, fields, ValidationError, validate

from hue import HueClient

log = logging.getLogger(__name__)

app = Flask(__name__)


class ActionSchema(Schema):
    on = fields.Boolean()
    bri = fields.Integer(validate=validate.Range(min=0, max=254))
    transitiontime = fields.Integer()
    hue = fields.Integer(validate=validate.Range(min=0, max=65535))
    sat = fields.Integer(validate=validate.Range(min=0, max=254))


@app.route('/hue/lights', methods=['GET'])
def hue_lights():
    return jsonify(HueClient().get_lights())


@app.route('/hue/rooms', methods=['GET'])
def hue_rooms():
    return jsonify(HueClient().get_rooms())


@app.route('/hue/lights/<int:hue_id>', methods=['PUT'])
def hue_update_light(hue_id: int):
    try:
        action = ActionSchema().load(request.get_json())
        log.info(action)
        result = HueClient().update_light(hue_id, action)
    except ValidationError as err:
        raise err
    return jsonify(result)


@app.route('/hue/rooms/<int:hue_id>', methods=['PUT'])
def hue_update_room(hue_id: int):
    try:
        action = ActionSchema().load(request.get_json())
        log.info(action)
        result = HueClient().update_room(hue_id, action)
    except ValidationError as err:
        raise err
    return jsonify(result)


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


if __name__ == '__main__':
    app.run(debug=True)
