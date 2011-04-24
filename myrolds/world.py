from myrolds.item import Item
from myrolds.util import enumerateItems, enumerateDoors


class World(object):

    def __init__(self):
        self.scapes = {}
        self.player = None
        startingPlace = None

    def setScapes(self, scapes):
        self.scapes = scapes

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
    def __init__(self, desc):
        self.desc = desc
        self.inv = []
        self.gameOver = False

    def enter(self,player):
        if self.gameOver:
            player.gameOver = True

    def addItem(self, it):
        self.inv.append(it)

    def removeItem(self,it):
        self.inv.remove(it)

    def describe(self):
        print self.desc
        visibleItems = [ it for it in self.inv if it.isVisible ]
        if len(visibleItems) > 1:
            print "There are %s here." % enumerateItems(visibleItems)
        else:
            print "There is %s here." % enumerateItems(visibleItems)

    def getExitName(self):
        return "exit"

    def listDoors(self):
        numDoors = sum([1 for door in self.doors if door is not None])
        if numDoors == 0:
            reply = "There are no doors in any direction."
        else:
            if numDoors == 1:
                reply = "There is a door to the "
            else:
                reply = "There are doors to the "
            doorNames = [{0:"north", 1:"south", 2:"east", 3:"west"}[index]
                         for index, door in enumerate(self.doors)
                         if door is not None]
            #~ print doorNames
            reply += enumerateDoors(doorNames)
            reply += "."
            print reply

    def describeAndListDoors(self):
        self.describe()
        self.listDoors()


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
        self.doors = [None,None,None,None]

    def __getattr__(self, attr):
        return {
            "n":self.doors[0],
            "s":self.doors[1],
            "e":self.doors[2],
            "w":self.doors[3],
            }[attr]

    def getExitName(self):
        return "door"


class Exit(Room):
    def __init__(self):
        super(Exit,self).__init__("")

    def enter(self,player):
        player.gameOver = True



