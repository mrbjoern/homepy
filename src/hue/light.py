from hue.action import Action


class Light(object):

    def __init__(self, hue_id, light):
        """
        :type hue_id: number
        :type light: dict
        """
        self.id = hue_id
        self.name = light['name']
        self.state = Action(light['state'])

    def __str__(self):
        return self.id
