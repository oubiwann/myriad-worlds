import random, signal, sys

from twisted.python import log

from myriad.const import (
    N, S, E, W, NE, NW, SE, SW, C, U, D, INVALID_EXIT, OK, SIGUSR1, SIGUSR2,
    signalLookup)


def aOrAn(item):
    if item.desc[0] in "aeiou":
        return "an"
    else:
        return "a"


def enumerateItems(items):
    if len(items) == 0:
        return "nothing"
    out = []
    for item in items:
        if len(items) > 1 and item == items[-1]:
            out.append("and")
        out.append(aOrAn(item))
        if item == items[-1]:
            out.append(item.desc)
        else:
            if len(items) > 2:
                out.append(item.desc + ",")
            else:
                out.append(item.desc)
    return " ".join(out)


def enumerateExits(l):
    if len(l) == 0: return ""
    out = []
    for item in l:
        if len(l) > 1 and item == l[-1]:
            out.append("and")
        if item == l[-1]:
            out.append(item)
        else:
            if len(l) > 2:
                out.append(item + ",")
            else:
                out.append(item)
    return " ".join(out)


def getRandomInts(min=0, max=1, step=1, count=1):
    max += step
    # XXX this needs to use the session randomizer... need to move this
    # function into a class that the session can get access to (the session has
    # access to the game, and thus the story, world, and player objects...
    # world has access to map objects, so that seems like a good place)
    return [random.randrange(min, max, step) for x in xrange(count)]


def getDirectionName(direction):
    if direction == N:
        return "north"
    elif direction == S:
        return "south"
    elif direction == E:
        return "east"
    elif direction == W:
        return "west"
    elif direction == NE:
        return "northeast"
    elif direction == SE:
        return "southeast"
    elif direction == SW:
        return "southwest"
    elif direction == NW:
        return "northwest"
    elif direction == C:
        return "center"
    elif direction == U:
        return "up"
    elif direction == D:
        return "down"


def renderBanner(template, gameBanner, help):
    return template.replace(
        "{{GAME_BANNER}}", gameBanner.strip()).replace(
        "{{HELP}}", help)


class SignalHandler(object):
    """
    """
    exitCode = OK

    def __init__(self):
        for signum in xrange(1, 32):
            if signum not in [signal.SIGKILL, signal.SIGSTOP]:
                signal.signal(signum, self.handle)

    def handle(self, signum, frame):
        self.exitCode = INVALID_EXIT + signum
        msg = "Received signal %s: '%s'; exiting with code %s" % (
            signum, signalLookup[signum], self.exitCode)
        print "\n" + msg
        log.msg(msg)
        sys.exit(self.exitCode)
