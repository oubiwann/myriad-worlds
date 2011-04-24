class Item(object):

    items = {}

    def __init__(self, name="", isDeadly=False, isFragile=False, isBroken=False,
                 isTakable=True, isVisible=True, isOpenable=False):
        self.desc = name
        self.isDeadly = isDeadly
        self.isFragile = isFragile
        self.isBroken = isBroken
        self.isTakeable = isTakable
        self.isVisible = isVisible
        self.isOpenable = isOpenable
        self.useAction = None
        self.usableConditionTest = None
        Item.items[name] = self

    def __str__(self):
        return self.desc

    def breakItem(self):
        if not self.isBroken:
            print "<Crash!>"
            self.desc = "broken " + self.desc
            self.isBroken = True

    def isUsable(self, player, target):
        if self.usableConditionTest:
            return self.usableConditionTest(player, target)
        else:
            return False

    def useItem(self, player, target):
        if self.useAction:
            self.useAction(player, self, target)


class OpenableItem(Item):
    def __init__(self, desc, contents = None):
        super(OpenableItem,self).__init__(desc)
        self.isOpenable = True
        self.isOpened = False
        self.contents = contents

    def openItem(self, player):
        if not self.isOpened:
            self.isOpened = True
            self.isOpenable = False
            if self.contents is not None:
                player.room.addItem( self.contents )
            self.desc = "open " + self.desc
