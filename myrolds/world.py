class Room(object):
    def __init__(self, desc):
        self.desc = desc
        self.inv = []
        self.gameOver = False
        self.doors = [None,None,None,None]

    def __getattr__(self,attr):
        return \
            {
            "n":self.doors[0],
            "s":self.doors[1],
            "e":self.doors[2],
            "w":self.doors[3],
            }[attr]

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
            print "There are %s here." % enumerateItems( visibleItems )
        else:
            print "There is %s here." % enumerateItems( visibleItems )


class Exit(Room):
    def __init__(self):
        super(Exit,self).__init__("")

    def enter(self,player):
        player.gameOver = True


def createRooms( rm ):
    """
    create rooms, using multiline string showing map layout
    string contains symbols for the following:
     A-Z, a-z indicate rooms, and rooms will be stored in a dictionary by
               reference letter
     -, | symbols indicate connection between rooms
     <, >, ^, . symbols indicate one-way connection between rooms
    """
    # start with empty dictionary of rooms
    ret = {}

    # look for room symbols, and initialize dictionary
    # - exit room is always marked 'Z'
    for c in rm:
        if "A" <= c <= "Z" or "a" <= c <= "z":
            if c != "Z":
                ret[c] = Room(c)
            else:
                ret[c] = Exit()

    # scan through input string looking for connections between rooms
    rows = rm.split("\n")
    for row,line in enumerate(rows):
        for col,c in enumerate(line):
            if "A" <= c <= "Z" or "a" <= c <= "z":
                room = ret[c]
                n = None
                s = None
                e = None
                w = None

                # look in neighboring cells for connection symbols (must take
                # care to guard that neighboring cells exist before testing
                # contents)
                if col > 0 and line[col-1] in "<-":
                    other = line[col-2]
                    w = ret[other]
                if col < len(line)-1 and line[col+1] in "->":
                    other = line[col+2]
                    e = ret[other]
                if row > 1 and col < len(rows[row-1]) and rows[row-1][col] in '|^':
                    other = rows[row-2][col]
                    n = ret[other]
                if row < len(rows)-1 and col < len(rows[row+1]) and rows[row+1][col] in '|.':
                    other = rows[row+2][col]
                    s = ret[other]

                # set connections to neighboring rooms
                room.doors=[n,s,e,w]
    return ret


# put items in rooms
def putItemInRoom(i,r):
    if isinstance(r,basestring):
        r = rooms[r]
    r.addItem( Item.items[i] )
