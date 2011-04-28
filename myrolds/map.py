from myrolds import util

from myrolds.const import N, S, E, W, NE, NW, SE, SW, C


directions = {
    N: 0,
    S: 1,
    E: 2,
    W: 3}
reverseDirections = dict([
    (index, direction) for direction, index in directions.items()])


def getDirectionName(abbr):
    if abbr.lower() == "n":
        return "north"
    elif abbr.lower() == "s":
        return "south"
    elif abbr.lower() == "e":
        return "east"
    elif abbr.lower() == "w":
        return "west"


class ASCIICharacterMap(object):
    """
    This class parses maps that have been created using ASCII characters.

    Because rooms are limited to A-Za-z, ASCII character-based maps are limited
    to 52 rooms/scapes.
    """
    def __init__(self, filename):
        self.scapes = {}
        self.file = open(filename)
        self.data = self.file.read()
        # with the string data from the file, instantiate rooms for all the
        # scapes
        self.createScapes(self.getData())

    def getData(self):
        return self.data

    def getScapes(self):
        return self.scapes

    def createScapes(self, map):
        """
        create rooms, using multiline string showing map layout
        string contains symbols for the following:

            A-Z, a-z indicate rooms, and rooms will be stored in a dictionary
                by reference letter

            -, | symbols indicate connection between rooms

            <, >, ^, . symbols indicate one-way connection between rooms
        """
        from myrolds.world import Exit, Room
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
                    if col < (len(line) - 1) and line[col + 1] in "->":
                        other = line[col + 2]
                        e = self.scapes[other]
                    if (row > 1
                        and col < len(rows[row - 1])
                        and rows[row - 1][col] in '|^'):
                        other = rows[row - 2][col]
                        n = self.scapes[other]
                    if (row < (len(rows) - 1)
                        and col < len(rows[row + 1])
                        and rows[row + 1][col] in '|.'):
                        other = rows[row + 2][col]
                        s = self.scapes[other]

                    # set connections to neighboring rooms
                    room.exits = [n, s, e, w]


class GeneratedMap(object):

    def __init__(self, size):
        self.size = size

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
            grid = util.createEmptyGrid(x, y)
            tile = util.getRandomTileClass()
            # let's get the first one started, and then start setting the
            # surrounding tiles
            grid[0][0] = tile
            util.setSurroundingTiles(tile, 0, 0, grid)
            # XXX debug
            for j in grid:
                for i in j:
                    if hasattr(i, "__name__"):
                        x = i.__name__
                    else:
                        x = i
                    print x.ljust(11, " "),
                print
        # enough tiles to hold 3-6 small towns
        if self.size == "small":
            pass
        # enough tiles to hold one large city and a good-sized boundary area
        if self.size == "medium":
            pass
        # enough tiles to hold something the size of a state in the US
        if self.size == "large":
            pass
        # enough tiles to hold one country
        if self.size == "huge":
            pass
        # enough tiles to hold a continent
        if self.size == "gigantic":
            pass
        # for all non-planetary sized grids, border tiles will be non-passable
        # at the edges
        util.setGridBoundaries(grid)
        # enough tiles to hold an Earth-sized planet
        if self.size == "planetary":
            pass

class Map(object):

    def __init__(self, mapData):
        self.type = mapData.get("type")
        self.data = None
        if self.type.lower() == "ascii":
            self.location = mapData.get("location")
            _map = ASCIICharacterMap(self.location)
            self.data = _map.getData()
            self.scapes = _map.getScapes()
        if self.type.lower() == "procedural":
            self.size = mapData.get("size")
            _map = GeneratedMap(self.size)
            self.data = _map.getData()
            self.scapes = _map.getScapes()

    def getData(self):
        return self.data

    def getScapes(self):
        return self.scapes
