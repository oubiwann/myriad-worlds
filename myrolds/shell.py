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
        useVerb = oneOf("USE U")
        openVerb = makeCmd("OPEN O")
        quitVerb = makeCmd("QUIT Q")
        lookVerb = makeCmd("LOOK L")
        doorsVerb = CaselessKeyword("DOORS")
        helpVerb = makeCmd("H HELP ?")
        readVerb = CaselessKeyword("READ")

        itemRef = OneOrMore(Word(alphas)).setParseAction(self.validateItemName)
        nDir = oneOf("N NORTH",caseless=True).setParseAction(replaceWith("N"))
        sDir = oneOf("S SOUTH",caseless=True).setParseAction(replaceWith("S"))
        eDir = oneOf("E EAST",caseless=True).setParseAction(replaceWith("E"))
        wDir = oneOf("W WEST",caseless=True).setParseAction(replaceWith("W"))
        moveDirection = nDir | sDir | eDir | wDir

        invCommand = invVerb
        dropCommand = dropVerb + itemRef.setResultsName("item")
        takeCommand = takeVerb + itemRef.setResultsName("item")
        useCommand = useVerb + itemRef.setResultsName("usedObj") + \
            Optional(oneOf("IN ON", caseless=True)) + \
            Optional(itemRef,default=None).setResultsName("targetObj")
        openCommand = openVerb + itemRef.setResultsName("item")
        moveCommand = moveVerb + moveDirection.setResultsName("direction")
        quitCommand = quitVerb
        lookCommand = lookVerb
        doorsCommand = doorsVerb
        helpCommand = helpVerb
        readCommand = readVerb + itemRef("subjectObj")

        invCommand.setParseAction(
            self.makeCommandParseAction(InventoryCommand))
        dropCommand.setParseAction(
            self.makeCommandParseAction(DropCommand))
        takeCommand.setParseAction(
            self.makeCommandParseAction(TakeCommand))
        useCommand.setParseAction(
            self.makeCommandParseAction(UseCommand))
        openCommand.setParseAction(
            self.makeCommandParseAction(OpenCommand))
        moveCommand.setParseAction(
            self.makeCommandParseAction(MoveCommand))
        quitCommand.setParseAction(
            self.makeCommandParseAction(QuitCommand))
        lookCommand.setParseAction(
            self.makeCommandParseAction(LookCommand))
        doorsCommand.setParseAction(
            self.makeCommandParseAction(DoorsCommand))
        helpCommand.setParseAction(
            self.makeCommandParseAction(HelpCommand))
        readCommand.setParseAction(
            self.makeCommandParseAction(ReadCommand))
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
