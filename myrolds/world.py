from myrolds.item import Item
from myrolds.util import enumerateItems


class World(object):

    def __init__(self):
        self.scapes = {}
        self.player = None

    def createScapes(self, map):
        """
        create rooms, using multiline string showing map layout
        string contains symbols for the following:
         A-Z, a-z indicate rooms, and rooms will be stored in a dictionary by
                   reference letter
         -, | symbols indicate connection between rooms
         <, >, ^, . symbols indicate one-way connection between rooms
        """
        # look for room symbols, and initialize dictionary
        # - exit room is always marked 'Z'
        for c in map:
            if "A" <= c <= "Z" or "a" <= c <= "z":
                if c != "Z":
                    self.scapes[c] = Room(c)
                else:
                    self.scapes[c] = Exit()
        # scan through input string looking for connections between rooms
        rows = map.split("\n")
        for row, line in enumerate(rows):
            for col, c in enumerate(line):
                if "A" <= c <= "Z" or "a" <= c <= "z":
                    room = self.scapes[c]
                    n = None
                    s = None
                    e = None
                    w = None
                    # look in neighboring cells for connection symbols (must
                    # take care to guard that neighboring cells exist before
                    # testing contents)
                    if col > 0 and line[col-1] in "<-":
                        other = line[col-2]
                        w = self.scapes[other]
                    if col < len(line)-1 and line[col+1] in "->":
                        other = line[col+2]
                        e = self.scapes[other]
                    if (row > 1 
                        and col < len(rows[row-1]) 
                        and rows[row-1][col] in '|^'):
                        other = rows[row-2][col]
                        n = self.scapes[other]
                    if (row < len(rows)-1 
                        and col < len(rows[row+1]) 
                        and rows[row+1][col] in '|.'):
                        other = rows[row+2][col]
                        s = self.scapes[other]

                    # set connections to neighboring rooms
                    room.doors = [n,s,e,w]

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


class Exit(Room):
    def __init__(self):
        super(Exit,self).__init__("")

    def enter(self,player):
        player.gameOver = True



