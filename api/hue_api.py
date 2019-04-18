import logging

from flask import Flask, jsonify, request, Blueprint
from marshmallow import Schema, fields, ValidationError, validate

from api.hue import HueClient

log = logging.getLogger(__name__)

bp = Blueprint('hue_api', __name__, url_prefix="/hue")


class ActionSchema(Schema):
    on = fields.Boolean()
    bri = fields.Integer(validate=validate.Range(min=0, max=254))
    transitiontime = fields.Integer()
    hue = fields.Integer(validate=validate.Range(min=0, max=65535))
    sat = fields.Integer(validate=validate.Range(min=0, max=254))


@bp.route('/lights', methods=['GET'])
def hue_lights():
    return jsonify(HueClient().get_lights())


@bp.route('/rooms', methods=['GET'])
def hue_rooms():
    return jsonify(HueClient().get_rooms())


@bp.route('/scenes', methods=['GET'])
def hue_scenes():
    return jsonify(HueClient().get_scenes())


@bp.route('/lights/<int:hue_id>', methods=['PUT'])
def hue_update_light(hue_id: int):
    try:
        action = ActionSchema().load(request.get_json())
        log.info(action)
        result = HueClient().update_light(hue_id, action)
    except ValidationError as err:
        raise err
    return jsonify(result)


@bp.route('/rooms/<int:hue_id>', methods=['PUT'])
def hue_update_room(hue_id: int):
    try:
        action = ActionSchema().load(request.get_json())
        log.info(action)
        result = HueClient().update_room(hue_id, action)
    except ValidationError as err:
        raise err
    return jsonify(result)


"""
@bp.errorhandler(404)
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
"""