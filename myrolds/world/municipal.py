from myrolds.world.base import Tile


class Town(Tile):

    def addBuilding(self, building):
        pass


class Building(Tile):

    def addRoom(self, room):
        pass


class Room(Tile):
    """
    A "tile" or "section" of the world. This can be of any size
    """
    def __init__(self, *args, **kwargs):
        super(Room, self).__init__(*args, **kwargs)
        self.exits = [None] * 8

    def getExitName(self):
        return "door"


class Exit(Room):
    def __init__(self):
        super(Exit, self).__init__("")

    def enter(self,player):
        player.gameOver = True
