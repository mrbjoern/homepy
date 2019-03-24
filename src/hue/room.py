class Room(object):

    def __init__(self, hue_id, room):
        """
        :param hue_id: number
        :param room: dict
        """
        self.id = hue_id
        self.name = room['name']
        self.action = room['action']

    def __str__(self):
        return self.name
