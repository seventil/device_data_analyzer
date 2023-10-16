""" pass
"""

class HardnessTesterData:
    """Class containing curent data received form ht"""
    def __init__(self):
        self.who = None
        self.b = None
        self.scale = None
        self.calib = None
        self.k = None
        self.h = None
        self.e = None
        self.name = None
        self.data = []

    def update_data(self, data: dict):
        for key, value in data.items():
            setattr(self, key.lower(), value)


def blt_connector_factory(class_key: str) -> None:
    """ pass
    """
    if class_key == "Simulation":
        # import stuff
        # return class
        return "Simulation class"
    if class_key == "Bleak":
        # import stuff
        # return class
        return "Simulation class"