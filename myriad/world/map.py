import itertools
import random

from pyparsing import srange

from myriad import util
from myriad.const import N, S, E, W, NE, SE, SW, NW, C, U, D
from myriad.world import terrain


# XXX we need to get rid of this; the directions are being pulled from
# myrolds.const now, and since the directions are now constants themselves,
# there's not need for a mapping... all dependent code should be updated to not
# use this
directions = {
    N: 0,
    S: 1,
    E: 2,
    W: 3}
reverseDirections = dict([
    (index, direction) for direction, index in directions.items()])
northConnectors = "^|"
southConnectors = "v|"
eastConnectors = ">-"
westConnectors = "<-"
neConnector = "/"
seConnector = "\\"
swConnector = "/"
nwConnector = "\\"
roomConnectorsOneWay = [x[0] for x in [
    northConnectors, southConnectors, eastConnectors, westConnectors]]
roomConnectorsTwoWay = [neConnector, seConnector] + [x[1] for x in [
    northConnectors, eastConnectors]]
roomConnectrosAll = roomConnectorsOneWay + roomConnectorsTwoWay
legalRoomKeys = ("""ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuwxyz"""
                 """0123456789!@#$%&*+=?[]{}:;'".,""")
exitKey = "Z"


class ASCIICharacterMap(object):
    """
    This class parses maps that have been created using ASCII characters.

    Because rooms are limited to legalRoomKeys, ASCII character-based maps are
    limited to len(legalRoomKeys) == 81 rooms/tile.
    """
    def __init__(self, filename=""):
        self.scapes = {}
        self.file = None
        self.data = None
        if filename:
            self.file = open(filename)
            self.data = self.file.read()
        # with the string data from the file, instantiate rooms for all the
        # scapes
        if self.data:
            self.createScapes(self.getData())

    def getData(self):
        return self.data

    def getScapes(self):
        return self.scapes

    def createScapes(self, map):
        """
        Create rooms, using a multi-line string showing map layout. The string
        contains symbols for the following:

            A-Z, a-u, w-z, 0-9, !@#$%&*+=?[]{}:;.,'" indicate rooms, and rooms
                will be stored in a dictionary by reference letter

            -, |, /, \ symbols indicate connection between rooms

            <, >, ^, v symbols indicate one-way connection between rooms
        """
        # XXX if we have to import these here to avoid circularity, then maybe
        # the classes have been placed in the wrong location. Look into this.
        from myriad.world.municipal import Exit, Room
        # If there is no new line at the beginning of the ASCII map, the
        # parseing will not be successful. Let's make sure there is.
        map.lstrip()
        map = "\n" + map
        # look for room symbols, and initialize dictionary
        for c in map:
            if c in legalRoomKeys:
                room = Room(c)
                if c == exitKey:
                    room = Exit()
                # XXX change to "tiles" instead of "scapes"
                self.scapes[c] = room
        # scan through input string looking for connections between rooms
        rows = map.split("\n")
        for row, line in enumerate(rows):
            for col, c in enumerate(line):
                if c not in legalRoomKeys:
                    continue
                room = self.scapes[c]
                n = None
                s = None
                e = None
                w = None
                ne = None
                se = None
                sw = None
                nw = None
                # look in neighboring cells for connection symbols (must
                # take care to guard that neighboring cells exist before
                # testing contents)
                if col > 1 and line[col - 1] in westConnectors:
                    other = line[col - 2]
                    w = self.scapes[other]
                if col < (len(line) - 1) and line[col + 1] in eastConnectors:
                    other = line[col + 2]
                    e = self.scapes[other]
                if (row > 2
                    and col < len(rows[row - 1])
                    and rows[row - 1][col] in northConnectors):
                    other = rows[row - 2][col]
                    n = self.scapes[other]
                if (row < (len(rows) - 1)
                    and col < len(rows[row + 1])
                    and rows[row + 1][col] in southConnectors):
                    other = rows[row + 2][col]
                    s = self.scapes[other]
                if (row > 2 
                    and col < len(rows[row - 1]) - 1 
                    and rows[row - 1][col + 1] == neConnector):
                    other = rows[row - 2][col + 2]
                    ne = self.scapes[other]
                if (row < len(rows) - 1 
                    and col < len(rows[row + 1]) - 1 
                    and rows[row + 1][col + 1] == seConnector):
                    other = rows[row + 2][col + 2]
                    se = self.scapes[other]
                if (row < len(rows) - 1 
                    and 1 < col < len(rows[row + 1]) + 1 
                    and rows[row + 1][col - 1] == swConnector):
                    other = rows[row + 2][col - 2]
                    sw = self.scapes[other]
                if (row > 2 
                    and 2 < col < len(rows[row - 1]) + 1 
                    and rows[row - 1][col - 1] == nwConnector):
                    other = rows[row - 2][col - 2]
                    nw = self.scapes[other]

                # set connections to neighboring rooms
                room.exits = [n, s, e, w, ne, se, sw, nw]


class GeneratedMap(object):

    def __init__(self, size):
        self.size = size
        self.grid = None
        self.startingTile = None
        self.passableTiles = []
        self.playableTiles = []
        self.generateTiles()
        self.finishTiles()

    def printTiles(self):
        for j in self.grid:
            for i in j:
                if hasattr(i, "__name__"):
                    x = i.__name__
                else:
                    x = i
                print x.ljust(11, " "),
            print

    def generateTiles(self):
        # enough tiles to hold 1-2 small towns
        if self.size == "tiny":
            # One town can fit in a 5x5 grid (77.5 sq. mi.); two can be crammed
            # into a 5x10 grid (155 sq. mi.), however, two would fit more
            # comfortably in a 10x10 (310 sq. mi.) or 10x15 grid (465 sq. mi.).
            min = 5
            max = 15
            step = 5
            (x, y) = util.getRandomInts(min=min, max=max, step=step, count=2)
            # XXX debug
            print "grid size: (%s, %s)" % (x, y)
            self.tileDimensions = (x, y)
            grid = createEmptyGrid(x, y)
            tile = terrain.getRandomTileClass()
            # let's get the first one started, and then start setting the
            # surrounding tiles
            grid[0][0] = tile
            setSurroundingTiles(tile, 0, 0, grid)
        # enough tiles to hold 3-6 small towns
        elif self.size == "small":
            pass
        # enough tiles to hold one large city and a good-sized boundary area
        elif self.size == "medium":
            pass
        # enough tiles to hold something the size of a state in the US
        elif self.size == "large":
            pass
        # enough tiles to hold one country
        elif self.size == "huge":
            pass
        # enough tiles to hold a continent
        elif self.size == "gigantic":
            pass
        # for all non-planetary sized grids, border tiles will be non-passable
        # at the edges
        # enough tiles to hold an Earth-sized planet
        elif self.size == "planetary":
            pass
        self.grid = grid
        # XXX debug
        self.printTiles()

    def finishTiles(self):
        """
        This method does the following, once the tiles have been generated:
            * instantiates the tile classes at each grid location
            * sets the exits on each tile
            * builds a list of tiles that are passable
            * builds a list of tiles that are playable (passable *and* have
              exits)
            * set the starting place for the player
        """
        for j, row in enumerate(self.grid):
            for i, tile in enumerate(row):
                tileInstance = tile()
                tileInstance.startingPlace = False
                # set the exits
                exits = getSurroundingExits(i, j, self.grid)
                tileInstance.exits = exits
                maxExits = len(tileInstance.exits)
                # get passable tiles
                if tileInstance.isPassable:
                    self.passableTiles.append(tileInstance)
                    # get playable tiles
                    nones = [exit for exit in tileInstance.exits
                             if exit is None]
                    if nones > maxExits:
                        self.playableTiles.append(tileInstance)
        # set one of the playable tiles as the starting place
        # XXX use randomizer for this? or do we always want to start in a new
        # place?
        self.startingTile = random.choice(self.getPlayableTiles())
        self.startingTile.startingPlace = True

    def getScapes(self):
        return self.grid

    def getPassableTiles(self):
        return self.passableTiles

    def getPlayableTiles(self):
        return self.playableTiles
            

class Map(object):

    def __init__(self, mapData):
        self.type = mapData.get("type")
        self.data = None
        self._map = None
        if self.type.lower() == "ascii":
            self.location = mapData.get("location")
            self._map = ASCIICharacterMap(self.location)
            self.data = self._map.getData()
        if self.type.lower() == "procedural":
            self.size = mapData.get("size")
            self._map = GeneratedMap(self.size)
        self.scapes = self._map.getScapes()

    def getData(self):
        return self.data

    def getScapes(self):
        return self.scapes

    def setStartingPlace(self, tile):
        self._map.startingTile = tile

    def getStartingPlace(self):
        return self._map.startingTile


def createEmptyGrid(x, y):
    return [[0] * x for j in xrange(y)]


def getSurroundingIndices(x, y, grid):
    """"
    Each tile will have 8 surrounding tiles, 4 for the 4 cardinal directions
    (n, s, e, w), and 4 for the intermediate directions (nw, ne, se, sw). Tiles
    at the edge will only wrap if 
    """
    maxXIndex = len(grid[0]) - 1
    maxYIndex = len(grid) - 1
    indices = {
        C: (x, y),
        NW: (x - 1, y - 1),
        N: (x, y - 1),
        NE: (x + 1, y - 1),
        E: (x + 1, y),
        SE: (x + 1, y + 1),
        S: (x, y + 1),
        SW: (x - 1, y + 1),
        W: (x - 1, y),
        }
    for direction, value in indices.items():
        if (-1 in value) or (value[0] > maxXIndex) or (value[1] > maxYIndex):
            indices[direction] = None
    return indices


def getSurroundingExits(x, y, grid):
    indices = getSurroundingIndices(x, y, grid)
    for direction, value in indices.items():
        if direction == C:
            continue
        elif not value:
            continue
        else:
            tile = grid[y][x]
            if not tile.isPassable:
                indices[direction] = None
    return [value for key, value in sorted(indices.items())]


def setSurroundingTiles(tile, x, y, grid):
    """
    For each random tile we select, we need to 1) make sure that it's a valid
    transition from all surrounding tiles, and 2) make sure that there are
    least two passable neighboring tiles.
    """
    neighbors = getSurroundingIndices(x, y, grid)
    neighborClasses = []
    emptyTiles = []
    for direction, coords in neighbors.items():
        # if the neighbor is off the grid (e.g., tile would be on the border),
        # skip it
        if not coords:
            continue
        (neighborX, neighborY) = coords
        neighborTile = grid[neighborY][neighborX]
        # let's track the tiles that need to be set
        if neighborTile == 0:
            emptyTiles.append((neighborX, neighborY))
        # let's separately track the tiles that have already been set
        elif issubclass(neighborTile, terrain.GeographicalFeature):
            neighborClasses.append(neighborTile)
        else:
            raise Exception("What *is* this tile?!?")
    for x, y in emptyTiles:
        grid[y][x] = terrain.getRandomTileTransitionClass(
            tile, neighborClasses)
    # once all the neighbors have been set, get the next unset (x, y) and
    # re-run; we'll use the eastern-most neighbor until we run out of tiles in
    # the current row
    neighbor = neighbors[E]
    if neighbor:
        newX, newY = neighbors[E]
    else:
        newX, newY = (0, y + 1)
    # this next checks for y values that are off the grid (which indicates that
    # we're done)
    if newY > len(grid):
        return
    # this collapses all the rows into a single array; if all the zeros have
    # been replaced with terrain classes, we're done
    if 0 not in itertools.chain(*grid):
        return
    setSurroundingTiles(grid[newY][newX], newX, newY, grid)


def setGridBoundaries(grid):
    """
    Set all boundary tiles as non-passable in off-grid directions.

    Grids that represent a blog (e.g., planetary sized grids) should not use
    this methods; those grids should instead wrap at their boundaries.
    """
    # set top tiles as unpassable in the N direction
    # set bottom tiles as unpassable in the S direction
    # set right tiles as unpassable in the E direction
    # set left tiles as unpassable in the W direction
