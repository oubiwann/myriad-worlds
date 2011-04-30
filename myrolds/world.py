from myrolds import map
from myrolds.item import Item
from myrolds.util import enumerateItems, enumerateExits


# XXX maybe there should be layers *and* a context object. For all operations
# that require a layer to be know, the current layer (context) could just be
# used...
class World(object):

    def __init__(self):
        self.scapes = {}
        self.player = None
        startingPlace = None

    def setScapes(self, scapes):
        # XXX scapes need to know which layer they belong to
        self.scapes = scapes

    def getScape(self, name):
        # XXX from which layer?
        return self.scapes[name]

    def putItemInScape(self, item, scape):
        # XXX items need to know which layer they belong to
        if isinstance(scape, basestring):
            scape = self.scapes[scape]
        scape.addItem(Item.items[item])

    def placeCharacterInScape(self, character, scape, isPlayer=False):
        # XXX characters need to know which layer they belong to
        character.moveTo(scape)
        if isPlayer:
            self.setPlayer(character)

    def setPlayer(self, player):
        self.player = player

    def setLayers(self, layers):
        self.layers = layers


class Tile(object):
    """
    An abstract portion of the world.
    """
    def __init__(self, id, name="", desc=""):
        self.id = id
        self.name = name
        self.desc = desc
        self.inv = []
        self.gameOver = False
        self.doors = [None] * 8

    def enter(self, player):
        if self.gameOver:
            player.gameOver = True

    def addItem(self, item):
        self.inv.append(item)

    def removeItem(self, item):
        self.inv.remove(item)

    def describe(self):
        print self.desc
        visibleItems = [item for item in self.inv if item.isVisible]
        if len(visibleItems) > 1:
            print "There are %s here." % enumerateItems(visibleItems)
        else:
            print "There is %s here." % enumerateItems(visibleItems)

    def getExitName(self):
        return "exit"

    def listExits(self):
        numExits = sum([1 for exit in self.exits if exit is not None])
        if numExits == 0:
            reply = "There are no %s in any direction." % self.getExitName()
        else:
            if numExits == 1:
                reply = "There is a %s to the " % self.getExitName()
            else:
                reply = "There are %ss to the " % self.getExitName()
            exitNames = [map.getDirectionName(map.reverseDirections[index])
                         for index, exit in enumerate(self.exits)
                         if exit is not None]
            reply += enumerateExits(exitNames)
            reply += "."
            print reply

    def describeAndListExits(self):
        self.describe()
        self.listExits()


class Moment(Tile):
    """
    A "scape" that takes place in time, rather than physical space.
    """


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
        self.exits = [None, None, None, None]

    def __getattr__(self, attr):
        return self.getExits()[attr]

    def getExits(self):
        exitCheks = [
            (key.lower(), self.exists[value]) for key, value in map.directions]
        import pdb;pdb.set_trace()
        return dict(exitChecks)

    def getExitName(self):
        return "door"


class Exit(Room):
    def __init__(self):
        super(Exit, self).__init__("")

    def enter(self,player):
        player.gameOver = True
