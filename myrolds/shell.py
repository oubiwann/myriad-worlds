import random

from pyparsing import alphas, empty, oneOf, replaceWith
from pyparsing import CaselessLiteral, OneOrMore, Optional, ParseException
from pyparsing import LineEnd, Word

from myrolds.command import DropCommand, InventoryCommand, TakeCommand
from myrolds.command import MoveCommand, OpenCommand, QuitCommand, UseCommand
from myrolds.command import DoorsCommand, HelpCommand, LookCommand
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
        invVerb = oneOf("INV INVENTORY I", caseless=True)
        dropVerb = oneOf("DROP LEAVE", caseless=True)
        takeVerb = oneOf("TAKE PICKUP", caseless=True) | \
            (CaselessLiteral("PICK") + CaselessLiteral("UP"))
        moveVerb = oneOf("MOVE GO", caseless=True) | empty
        useVerb = oneOf("USE U", caseless=True)
        openVerb = oneOf("OPEN O", caseless=True)
        quitVerb = oneOf("QUIT Q", caseless=True)
        lookVerb = oneOf("LOOK L", caseless=True)
        doorsVerb = CaselessLiteral("DOORS")
        helpVerb = oneOf("H HELP ?",caseless=True)

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
            Optional(oneOf("IN ON",caseless=True)) + \
            Optional(itemRef,default=None).setResultsName("targetObj")
        openCommand = openVerb + itemRef.setResultsName("item")
        moveCommand = moveVerb + moveDirection.setResultsName("direction")
        quitCommand = quitVerb
        lookCommand = lookVerb
        doorsCommand = doorsVerb
        helpCommand = helpVerb

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

        return (invCommand |
                  useCommand |
                  openCommand |
                  dropCommand |
                  takeCommand |
                  moveCommand |
                  lookCommand |
                  doorsCommand |
                  helpCommand |
                  quitCommand).setResultsName("command") + LineEnd()

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
