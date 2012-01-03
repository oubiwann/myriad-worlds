class Item(object):

    items = {}

    def __init__(self, name="", isDeadly=False, isFragile=False, isBroken=False,
                 isTakable=True, isVisible=True):
        self.desc = name
        self.isDeadly = isDeadly
        self.isFragile = isFragile
        self.isBroken = isBroken
        self.breakableConditionTest = None
        self.isTakeable = isTakable
        self.isVisible = isVisible
        self.useAction = None
        self.usableConditionTest = None
        Item.items[name] = self

    def __str__(self):
        return self.desc

    def isBreakable(self, player, target):
        if self.breakableConditionTest:
            return self.breakableConditionTest(player, target)
        else:
            return False

    def breakItem(self):
        if not self.isBroken:
            print "*Crash!*"
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

    def __init__(self, desc, contents=None, *args, **kwargs):
        super(OpenableItem, self).__init__(desc, *args, **kwargs)
        self.isOpened = False
        self.openAction = None
        self.openableConditionTest = None
        self.contents = contents

    def isOpenable(self, player, target):
        if self.openableConditionTest:
            return self.openableConditionTest(player, target)
        else:
            return False

    def openItem(self, player):
        if not self.isOpened:
            self.isOpened = True
            self.isOpenable = False
            if self.contents is not None:
                [player.room.addItem(x) for x in self.contents]
            self.desc = "open " + self.desc


class ReadableItem(Item):

    def __init__(self, *args, **kwargs):
        super(ReadableItem, self).__init__(*args, **kwargs)
        self.isRead = False
        self.readAction = None
        self.readableConditionTest = None

    def isReadable(self, player, target):
        if self.readableConditionTest:
            return self.readableConditionTest(player, target)
        else:
            return False

    def readItem(self, player, target):
        if self.readAction:
            self.readAction(player, self, target)
