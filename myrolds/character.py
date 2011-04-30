class Player(object):

    def __init__(self, name):
        self.name = name
        self.gameOver = False
        self.inv = []

    def moveTo(self, room):
        self.room = room
        room.enter(self)
        if self.gameOver:
            if room.desc:
                room.describe()
            print "Game over!"
        else:
            room.describeAndListExits()

    def take(self, item):
        if item.isDeadly:
            print 'In despair, you yell, "Aaaagh! The %s..."' % item
            print "You're dead."
            self.gameOver = True
        else:
            self.inv.append(item)

    def drop(self, item):
        self.inv.remove(item)
        if item.isFragile:
            item.breakItem()
