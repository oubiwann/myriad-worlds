class Player(object):
    def __init__(self, name):
        self.name = name
        self.gameOver = False
        self.inv = []

    def moveTo(self, rm):
        self.room = rm
        rm.enter(self)
        if self.gameOver:
            if rm.desc:
                rm.describe()
            print "Game over!"
        else:
            rm.describe()

    def take(self,it):
        if it.isDeadly:
            print "Aaaagh!...., the %s killed me!" % it
            self.gameOver = True
        else:
            self.inv.append(it)

    def drop(self,it):
        self.inv.remove(it)
        if it.isFragile:
            it.breakItem()
