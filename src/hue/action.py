class Action(object):

    def __init__(self, action: dict):
        self.on = action['on']
        if action['bri'] > 255:
            self.bri = 255
        else:
            self.bri = action['bri']
        self.alert = action['alert']
