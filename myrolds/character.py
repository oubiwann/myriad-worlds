from myrolds.common import InventoriedObject


class Character(InventoriedObject):

    def __init__(self, name):
        super(Character, self).__init__()
        self.name = name

    # XXX change "room" to something more generic, e.g., "tile"
    def moveTo(self, room):
        self.room = room
        # XXX rooms need the ability to announce to everyone present that
        # soneone has just entered them
        room.enter(self)

    def drop(self, item):
        self.inv.remove(item)
        if item.isFragile:
            item.breakItem()


class NPC(Character):
    pass


class Player(Character):

    def __init__(self, name):
        super(Player, self).__init__(name)
        self.gameOver = False

    def moveTo(self, room):
        super(Player, self).moveTo(room)
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

