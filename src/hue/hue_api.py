import json
import logging

import requests
import yaml

from hue.action import Action
from hue.light import Light
from hue.room import Room

log = logging.getLogger(__name__)


class HueApi(object):

    def __init__(self):
        with open('config.yaml', 'r') as file:
            config = yaml.load(file, Loader=yaml.SafeLoader)
            username = config['hue']['username']
        discovery_result = requests.get('https://discovery.meethue.com/')
        if not discovery_result:
            log.error('No bridges found')
            return
        hue_internal_ip = discovery_result.json()[0]['internalipaddress']
        self._url = 'http://' + hue_internal_ip + '/api/' + username

    def _get(self, endpoint: str):
        """
        Get request on endpoint and handle possible errors
        :param endpoint: string
        :return:
        """
        return requests.get(self._url + endpoint).json()

    def _put(self, endpoint: str, action: Action):
        """
        Applies an action to a resource
        :param endpoint: string
        :param action: dict of actions
        :return: result of action
        """
        return requests.put(self._url + endpoint, json.dumps(action.__dict__)).json()

    def get_lights(self):
        """
        Get all lights registered with the Hue Bridge
        :return: List of Light objects
        """
        result = self._get('/lights')
        lights = []
        for key, value in result.items():
            lights.append(Light(key, value))
        return lights
    
    def update_light(self, hue_id: int, action: Action):
        """
        Update a light resource
        :param hue_id:
        :param action:
        :return:
        """
        return self._put('/lights/' + hue_id.__str__() + '/state', action)

    def get_rooms(self):
        """
        Get all rooms registered with the Hue Bridge
        :return: List of Room objects
        """
        result = self._get('/groups')
        rooms = []
        for key, value in result.items():
            if value['type'] == 'Room':
                rooms.append(Room(key, value))
        return rooms

    def update_room(self, hue_id: int, action: Action):
        """
        Update a light resource
        :param hue_id:
        :param action:
        :return:
        """
        return self._put('/groups/' + hue_id.__str__() + '/action', action)

    def get_schedules(self):
        return requests.get(self._url + '/schedules').json()

    def get_scenes(self):
        return requests.get(self._url + '/scenes').json()
