from myrolds.item import Item
from myrolds.util import enumerateItems, enumerateExits


class World(object):

    def __init__(self):
        self.scapes = {}
        self.player = None
        startingPlace = None

    def setScapes(self, scapes):
        self.scapes = scapes

    def getScape(self, name):
        return self.scapes[name]

    def putItemInScape(self, item, scape):
        if isinstance(scape, basestring):
            scape = self.scapes[scape]
        scape.addItem(Item.items[item])

    def placeCharacterInScape(self, character, scape, isPlayer=False):
        character.moveTo(scape)
        if isPlayer:
            self.setPlayer(character)

    def setPlayer(self, player):
        self.player = player


class WorldScape(object):
    """
    An abstract scape of the world.
    """
    def __init__(self, id, name="", desc=""):
        self.id = id
        self.name = name
        self.desc = desc
        self.inv = []
        self.gameOver = False

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
                reply = "There are %s to the " % self.getExitName()
            exitNames = [{0:"north", 1:"south", 2:"east", 3:"west"}[index]
                         for index, exit in enumerate(self.exits)
                         if exit is not None]
            reply += enumerateExits(exitNames)
            reply += "."
            print reply

    def describeAndListExits(self):
        self.describe()
        self.listExits()


class Moment(WorldScape):
    """
    A "scape" that takes place in time, rather than physical space.
    """


class Room(WorldScape):
    """
    A tile or section of the world. This
    """
    def __init__(self, *args, **kwargs):
        super(Room, self).__init__(*args, **kwargs)
        self.exits = [None,None,None,None]

    def __getattr__(self, attr):
        return {
            "n":self.exits[0],
            "s":self.exits[1],
            "e":self.exits[2],
            "w":self.exits[3],
            }[attr]

    def getExitName(self):
        return "door"


class Exit(Room):
    def __init__(self):
        super(Exit, self).__init__("")

    def enter(self,player):
        player.gameOver = True
