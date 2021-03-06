from myriad import util
from myriad.const import N, S, E, W, NE, NW, SE, SW, C
from myriad.item import Item


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
        print self.verbProg.capitalize() + "..."
        self._doCommand(player)


class MoveCommand(Command):
    def __init__(self, quals):
        super(MoveCommand,self).__init__("MOVE", "moving")
        self.direction = eval(quals["direction"])

    @staticmethod
    def helpDescription():
        return ("MOVE or GO - go NORTH, SOUTH, EAST, WEST, NORTHEAST, "
                "SOUTHEAST, SOUTHWEST, or NORTHWEST\n    (can abbreviate "
                "as 'GO N' and 'GO SW', or even just 'E' or 'SE')")

    def _doCommand(self, player):
        room = player.room
        nextRoom = room.exits[self.direction]
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
            print "You don't have %s %s." % (util.aOrAn(subj), subj)


class InventoryCommand(Command):
    def __init__(self, quals):
        super(InventoryCommand,self).__init__("INV", "taking inventory")

    @staticmethod
    def helpDescription():
        return "INVENTORY or INV or I - lists what items you have"

    def _doCommand(self, player):
        print "You have %s." % util.enumerateItems(player.inv)


class MapCommand(Command):
    def __init__(self, quals):
        super(MapCommand,self).__init__("MAP", "displaying map")
        self.quals = quals

    @staticmethod
    def helpDescription():
        return "MAP or M - lists what items you have"

    def _doCommand(self, player):
        # XXX limit this to display only 1) rooms actually visited, and 2)
        # hallways visible from the current location (if one hasn't visited the
        # connected rooms).
        print
        print player.story.map.getData()


class LookCommand(Command):
    def __init__(self, quals):
        super(LookCommand, self).__init__("LOOK", "looking")

    @staticmethod
    def helpDescription():
        return "LOOK or L - describes the current room and any objects in it"

    def _doCommand(self, player):
        player.room.printDescriptionAndExits()


class DoorsCommand(Command):
    def __init__(self, quals):
        super(DoorsCommand, self).__init__("DOORS", "looking for doors")

    @staticmethod
    def helpDescription():
        return "DOORS - display what doors are visible from this room"

    def _doCommand(self, player):
        player.room.printExits()


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
        availItems = room.inv + player.inv
        if self.subject in availItems:
            if self.subject.isUsable(player, self.target):
                self.subject.useItem(player, self.target)
            else:
                print "You can't use that here."
        else:
            print "There is no %s here to use." % self.subject


class ReadCommand(Command):
    def __init__(self, quals):
        super(ReadCommand,self).__init__("READ", "reading")
        self.subject = Item.items[quals["subjectObj"]]

    @staticmethod
    def helpDescription():
        return "READ - read an object, either in the room or the player's inventory"
        
    def _doCommand(self, player):
        rm = player.room
        availItems = rm.inv + player.inv
        if self.subject in availItems:
            if self.subject.isReadable(player, self.subject):
                self.subject.readItem(player, self.subject)
            else:
                print "There is nothing on that to read."
        else:
            print "There is no %s here to read." % self.subject


class OpenCommand(Command):
    def __init__(self, quals):
        super(OpenCommand,self).__init__("OPEN", "opening")
        self.subject = Item.items[quals["item"]]

    @staticmethod
    def helpDescription():
        return "OPEN or O - open an object"

    def _doCommand(self, player):
        rm = player.room
        availItems = rm.inv + player.inv
        if self.subject in availItems:
            if self.subject.has("isOpenable") and self.subject.isOpenable:
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
            ReadCommand,
            ]:
            print "  - %s" % cmd.helpDescription()
        print
