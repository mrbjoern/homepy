import json
import logging

import requests

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')

log = logging.getLogger(__name__)

class HueClient(object):

    def __init__(self):
        username = 'CjhNc-JgP8sNLg8LCdAjHh59q7YBlgUF6MuNSWNq'
        discovery_result = requests.get('https://discovery.meethue.com/')
        if not discovery_result:
            log.error('No bridges found')
            return
        hue_internal_ip = discovery_result.json()[0]['internalipaddress']
        self._url = 'http://' + hue_internal_ip + '/api/' + username

    def get_lights():
        lights = requests.get(self._url + '/lights').json()
        log.info(lights)
        for key,value in lights.items():
            Light(key, value)

        data = { 'on': True }
        result2 = requests.put(self._url + '/groups/1/action', data=json.dumps(data))
        print(result2.json())


class Light(object):

    def __init__(self, id, light):
        self.id = id
        self.name = light['name']
        self.state = light['state']
        log.info('id %s, name %s', self.id, self.name)
        log.info(self.state)

HueClient()
