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


class Map(object):
    
    def __init__(self, mapData):
        self.type = mapData.get("type")
        self.location = mapData.get("location")
        self.data = None
        if self.type.lower() == "ascii":
            _map = ASCIICharacterMap(self.location)
        self.data = _map.getData()
        self.scapes = _map.getScapes()

    def getData(self):
        return self.data

    def getScapes(self):
        return self.scapes
