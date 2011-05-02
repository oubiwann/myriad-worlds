from myrolds.common import InventoriedObject


class Player(InventoriedObject):

    def __init__(self, name):
        super(Player, self).__init__()
        self.name = name
        self.gameOver = False

    # XXX change "room" to something more generic, e.g., "tile"
    def moveTo(self, room):
        self.room = room
        room.enter(self)
        if self.gameOver:
            if room.desc:
                room.printDescription()
            print "Game over!"
        else:
            room.printDescriptionAndExits()

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
