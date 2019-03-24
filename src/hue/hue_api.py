import json
import logging

import requests
import yaml

log = logging.getLogger(__name__)


def get_sub_dict(dictionary, *argv):
    subset = {}
    for key, value in dictionary.items():
        log.info(value)
        subset[key] = ({k: value[k] for k in argv})
    log.info(subset)
    return subset


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

    def _put(self, endpoint: str, action):
        """
        Applies an action to a resource
        :param endpoint: string
        :param action: dict of actions
        :return: result of action
        """
        log.info(json.dumps(action))
        return requests.put(self._url + endpoint, json.dumps(action)).json()

    def get_lights(self):
        """
        Get all lights registered with the Hue Bridge
        :return: A filtered list of lights
        """
        result = self._get('/lights')
        return get_sub_dict(result, 'name', 'state')
    
    def update_light(self, hue_id: int, action):
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
        return get_sub_dict(result, 'name', 'state', 'lights')

    def update_room(self, hue_id: int, action):
        """
        Update a light resource
        :param hue_id:
        :param action:
        :return:
        """
        return self._put('/groups/' + hue_id.__str__() + '/action', action)

    def get_schedules(self):
        result = self._get('/schedules')
        return get_sub_dict(result, 'name', 'state')

    def get_scenes(self):
        result = self._get('/scenes')
        return get_sub_dict(result, 'name', 'state')
