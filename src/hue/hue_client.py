import logging

from hue import HueApi
from hue.action import Action

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')

log = logging.getLogger(__name__)


class HueClient(object):

    def __init__(self):
        self._hue_api = HueApi()
        """
        lights = self._hue_api.get_lights()
        for light in lights:
            log.info(light)
        rooms = self._hue_api.get_rooms()
        for room in rooms:
            log.info(room)
        action = Action({'on': True, 'bri': 255, 'alert': 'select'})
        result = self._hue_api.update_room(rooms[3], action)
        log.info(result)
        """

    def get_lights(self):
        return self._hue_api.get_lights()

    def get_rooms(self):
        return self._hue_api.get_rooms()


HueClient()
