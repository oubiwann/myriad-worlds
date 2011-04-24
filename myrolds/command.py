from myrolds.item import Item
from myrolds.util import aOrAn, enumerateDoors, enumerateItems


class Command(object):
    "Base class for commands"
    def __init__(self, verb, verbProg):
        self.verb = verb
        self.verbProg = verbProg

    @staticmethod
    def helpDescription():
        return ""

    def _doCommand(self, player):
        pass

    def __call__(self, player):
        print self.verbProg.capitalize()+"..."
        self._doCommand(player)


class MoveCommand(Command):
    def __init__(self, quals):
        super(MoveCommand,self).__init__("MOVE", "moving")
        self.direction = quals["direction"][0]

    @staticmethod
    def helpDescription():
        return """MOVE or GO - go NORTH, SOUTH, EAST, or WEST
          (can abbreviate as 'GO N' and 'GO W', or even just 'E' and 'S')"""

    def _doCommand(self, player):
        room = player.room
        nextRoom = room.doors[
            {
            "N":0,
            "S":1,
            "E":2,
            "W":3,
            }[self.direction]
            ]
        if nextRoom:
            player.moveTo(nextRoom)
        else:
            print "Can't go that way."


class TakeCommand(Command):
    def __init__(self, quals):
        super(TakeCommand,self).__init__("TAKE", "taking")
        self.subject = quals["item"]

    @staticmethod
    def helpDescription():
        return (
            "TAKE or PICKUP or PICK UP - pick up an object"
            "(but some are deadly)")

    def _doCommand(self, player):
        rm = player.room
        subj = Item.items[self.subject]
        if subj in rm.inv and subj.isVisible:
            if subj.isTakeable:
                rm.removeItem(subj)
                player.take(subj)
            else:
                print "You can't take that!"
        else:
            print "There is no %s here." % subj


class DropCommand(Command):
    def __init__(self, quals):
        super(DropCommand,self).__init__("DROP", "dropping")
        self.subject = quals["item"]

    @staticmethod
    def helpDescription():
        return "DROP or LEAVE - drop an object (but fragile items may break)"

    def _doCommand(self, player):
        rm = player.room
        subj = Item.items[self.subject]
        if subj in player.inv:
            rm.addItem(subj)
            player.drop(subj)
        else:
            print "You don't have %s %s." % (aOrAn(subj), subj)


class InventoryCommand(Command):
    def __init__(self, quals):
        super(InventoryCommand,self).__init__("INV", "taking inventory")

    @staticmethod
    def helpDescription():
        return "INVENTORY or INV or I - lists what items you have"

    def _doCommand(self, player):
        print "You have %s." % enumerateItems(player.inv)


class LookCommand(Command):
    def __init__(self, quals):
        super(LookCommand, self).__init__("LOOK", "looking")

    @staticmethod
    def helpDescription():
        return "LOOK or L - describes the current room and any objects in it"

    def _doCommand(self, player):
        player.room.describeAndListDoors()


class DoorsCommand(Command):
    def __init__(self, quals):
        super(DoorsCommand, self).__init__("DOORS", "looking for doors")

    @staticmethod
    def helpDescription():
        return "DOORS - display what doors are visible from this room"

    def _doCommand(self, player):
        player.room.listDoors()


class UseCommand(Command):
    def __init__(self, quals):
        super(UseCommand,self).__init__("USE", "using")
        self.subject = Item.items[quals["usedObj"]]
        if "targetObj" in quals.keys() and quals["targetObj"]:
            self.target = Item.items[quals["targetObj"]]
        else:
            self.target = None

    @staticmethod
    def helpDescription():
        return "USE or U - use an object, optionally IN or ON another object"

    def _doCommand(self, player):
        room = player.room
        availItems = room.inv+player.inv
        if self.subject in availItems:
            if self.subject.isUsable(player, self.target):
                self.subject.useItem(player, self.target)
            else:
                print "You can't use that here."
        else:
            print "There is no %s here to use." % self.subject


class OpenCommand(Command):
    def __init__(self, quals):
        super(OpenCommand,self).__init__("OPEN", "opening")
        self.subject = Item.items[ quals["item"] ]

    @staticmethod
    def helpDescription():
        return "OPEN or O - open an object"

    def _doCommand(self, player):
        rm = player.room
        availItems = rm.inv+player.inv
        if self.subject in availItems:
            if self.subject.isOpenable:
                self.subject.openItem(player)
            else:
                print "You can't use that here."
        else:
            print "There is no %s here to use." % self.subject


class QuitCommand(Command):
    def __init__(self, quals):
        super(QuitCommand,self).__init__("QUIT", "quitting")

    @staticmethod
    def helpDescription():
        return "QUIT or Q - ends the game"

    def _doCommand(self, player):
        print "Ok...."
        player.gameOver = True


class HelpCommand(Command):
    def __init__(self, quals):
        super(HelpCommand,self).__init__("HELP", "helping")

    @staticmethod
    def helpDescription():
        return "HELP or H or ? - displays this help message"

    def _doCommand(self, player):
        print "Enter any of the following commands (not case sensitive):"
        for cmd in [
            InventoryCommand,
            DropCommand,
            TakeCommand,
            UseCommand,
            OpenCommand,
            MoveCommand,
            LookCommand,
            DoorsCommand,
            QuitCommand,
            HelpCommand,
            ]:
            print "  - %s" % cmd.helpDescription()
        print
