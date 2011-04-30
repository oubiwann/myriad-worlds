import random

from pyparsing import alphas, empty, oneOf, replaceWith
from pyparsing import CaselessLiteral, OneOrMore, Optional, ParseException
from pyparsing import CaselessKeyword, LineEnd, MatchFirst, Word

from myrolds.command import DropCommand, InventoryCommand, TakeCommand
from myrolds.command import MoveCommand, OpenCommand, QuitCommand, UseCommand
from myrolds.command import DoorsCommand, HelpCommand, LookCommand, ReadCommand
from myrolds.item import Item
from myrolds.util import aOrAn


class ShellParseException(ParseException):
    pass


class ShellParser(object):
    def __init__(self, session=None):
        self.session = session
        self.bnf = self.makeBNF()

    def makeCommandParseAction(self, cls):
        def cmdParseAction(s, l, tokens):
            return cls(tokens)
        return cmdParseAction

    def makeBNF(self):
        makeCmd = lambda s: MatchFirst(map(CaselessKeyword, s.split()))
        invVerb = makeCmd("INV INVENTORY I")
        dropVerb = makeCmd("DROP LEAVE")
        takeVerb = makeCmd("TAKE PICKUP") | \
            (CaselessLiteral("PICK") + CaselessLiteral("UP"))
        moveVerb = makeCmd("MOVE GO") | empty
        useVerb = makeCmd("USE U")
        openVerb = makeCmd("OPEN O")
        quitVerb = makeCmd("QUIT Q")
        lookVerb = makeCmd("LOOK L")
        doorsVerb = CaselessKeyword("DOORS")
        helpVerb = makeCmd("H HELP ?")
        readVerb = CaselessKeyword("READ")

        itemRef = OneOrMore(Word(alphas)).setParseAction(self.validateItemName)
        makeDir = lambda s : makeCmd(s).setParseAction(
            replaceWith(s.split()[0]))
        nDir = makeDir("N NORTH")
        sDir = makeDir("S SOUTH")
        eDir = makeDir("E EAST")
        wDir = makeDir("W WEST")
        neDir = makeDir("NE NORTHEAST")
        seDir = makeDir("SE SOUTHEAST")
        swDir = makeDir("SW SOUTHWEST")
        nwDir = makeDir("NW NORTHWEST")
        moveDirection = nDir | sDir | eDir | wDir | neDir | seDir | swDir \
            | nwDir

        invCommand = invVerb
        dropCommand = dropVerb + itemRef("item")
        takeCommand = takeVerb + itemRef("item")
        useCommand = useVerb + itemRef("usedObj") + \
            Optional(oneOf("IN ON", caseless=True)) + \
            Optional(itemRef, default=None)("targetObj")
        openCommand = openVerb + itemRef("item")
        moveCommand = moveVerb + moveDirection("direction")
        quitCommand = quitVerb
        lookCommand = lookVerb
        doorsCommand = doorsVerb
        helpCommand = helpVerb
        readCommand = readVerb + itemRef("subjectObj")

        invCommand.setParseAction(InventoryCommand)
        dropCommand.setParseAction(DropCommand)
        takeCommand.setParseAction(TakeCommand)
        useCommand.setParseAction(UseCommand)
        openCommand.setParseAction(OpenCommand)
        moveCommand.setParseAction(MoveCommand)
        quitCommand.setParseAction(QuitCommand)
        lookCommand.setParseAction(LookCommand)
        doorsCommand.setParseAction(DoorsCommand)
        helpCommand.setParseAction(HelpCommand)
        readCommand.setParseAction(ReadCommand)
        return (invCommand |
                  useCommand |
                  openCommand |
                  dropCommand |
                  takeCommand |
                  moveCommand |
                  lookCommand |
                  doorsCommand |
                  helpCommand |
                  quitCommand |
                  readCommand).setResultsName("command") + LineEnd()

    def validateItemName(self, s, l, t):
        iname = " ".join(t)
        if iname not in Item.items:
            raise ShellParseException(s, l, "No such item '%s'." % iname)
        return iname

    def parseCmd(self, cmdstr):
        try:
            ret = self.bnf.parseString(cmdstr)
            return ret
        except ShellParseException, parseError:
            print parseError.msg
        except ParseException, parseError:
            print random.choice(["Sorry, I don't understand that.",
                                 "Say what?",
                                 "Whatchyoo talkin' 'bout, Willis?",
                                 "Huh?",
                                 "Garbage in, garbage out. Try again.",
                                 "What was the middle part again?",
                                 "Excuse me?",
                                 "Wtf?",
                                 "What?"])
