import textwrap

from myriad import const
from myriad import util


class InventoriedObject(object):

    def __init__(self):
        self.inv = []

    def addItem(self, item):
        self.inv.append(item)

    def removeItem(self, item):
        self.inv.remove(item)


class DescribedObject(object):

    def __init__(self, desc=""):
        self.isPassable = True
        self.desc = desc

    def getDescription(self):
        output = textwrap.fill(self.desc)
        visibleItems = [item for item in self.inv if item.isVisible]
        output += "\n\n"
        if len(visibleItems) > 1:
            output += "There are %s here." % util.enumerateItems(visibleItems)
        else:
            output += "There is %s here." % util.enumerateItems(visibleItems)
        return output

    def printDescription(self):
        print self.getDescription()


class TraversedObject(object):

    def __init__(self):
        self.isPassable = True
        self.doors = [None] * len(const.directions)
        self.gameOver = False

    def getExitName(self):
        return "exit"

    def getExits(self):
        reply = "\n"
        numExits = sum([1 for exit in self.exits if exit is not None])
        if numExits == 0:
            reply += "There are no %s in any direction." % self.getExitName()
        else:
            if numExits == 1:
                reply += "There is a %s to the " % self.getExitName()
            else:
                reply += "There are %ss to the " % self.getExitName()
            exitNames = [util.getDirectionName(exit)
                         for exit, room in enumerate(self.exits)
                         if room is not None]
            reply += util.enumerateExits(exitNames)
            reply += "."
            return reply

    def printExits(self):
        print self.getExits()
