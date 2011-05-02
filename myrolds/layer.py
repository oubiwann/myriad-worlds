class Layers(object):

    def __init__(self):
        self.worlds = {}

    def addWorld(self, world):
        self.worlds[world.name] = world


class Context(object):
    pass
