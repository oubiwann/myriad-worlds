from myriad.common import DescribedObject, InventoriedObject, TraversedObject
from myriad.item import Item


# XXX maybe there should be layers *and* a context object. For all operations
# that require a layer to be known, the current layer (context) could just be
# used...
class World(object):
    """
    """
    def __init__(self, name="Ordinary World", map=None, physics=None):
        self.name = name
        self.map = map
        self.physics = physics
        self.scapes = {}
        self.player = None
        self.startingPlace = None

    def setMap(self, map):
        self.map = map

    def getMap(self):
        return self.map

    def setScapes(self, scapes):
        # XXX scapes need to know which layer they belong to
        # 
        # XXX actually, they don't -- scapes added to a world just belong to
        # that world. The story needs to know about context (which world in the
        # layer is active), and that should be about it
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


class Tile(InventoriedObject, DescribedObject, TraversedObject):
    """
    An abstract portion of the world.
    """
    def __init__(self, id="", name="", desc=""):
        super(Tile, self).__init__()
        InventoriedObject.__init__(self)
        DescribedObject.__init__(self, desc)
        TraversedObject.__init__(self)
        self.id = id
        self.name = name

    def enter(self, player):
        if self.gameOver:
            player.gameOver = True

    def getDescriptionAndExits(self):
        return "%s\n%s" % (
            self.getDescription(), self.getExits())

    def printDescriptionAndExits(self):
        print getDescriptionAndExits()


class Moment(Tile):
    """
    A "scape" that takes place in time, rather than physical space.
    """
