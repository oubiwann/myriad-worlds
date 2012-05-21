import random, signal, sys

from dreamssh.sdk import interfaces, registry

from myriad import const


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
    if direction == const.N:
        return "north"
    elif direction == const.S:
        return "south"
    elif direction == const.E:
        return "east"
    elif direction == const.W:
        return "west"
    elif direction == const.NE:
        return "northeast"
    elif direction == const.SE:
        return "southeast"
    elif direction == const.SW:
        return "southwest"
    elif direction == const.NW:
        return "northwest"
    elif direction == const.C:
        return "center"
    elif direction == const.U:
        return "up"
    elif direction == const.D:
        return "down"


def renderBanner(template, gameBanner, help):
    return template.replace(
        "{{GAME_BANNER}}", gameBanner.strip()).replace(
        "{{HELP}}", help)


def setupLogging(logfile, type=const.LOCAL):
    """
    Set up logging to be Twisted compatible.
    """
    if type == const.LOCAL:
        import logging as log
        log.msg = log.info
        log.basicConfig(filename=logfile, level=log.INFO)
    else:
        from twisted.python import log
    registry.registerComponent(log, interfaces.ILogger)


class SignalHandler(object):
    """
    """
    exitCode = const.OK

    def __init__(self):
        for signum in xrange(1, 32):
            if signum not in [signal.SIGKILL, signal.SIGSTOP]:
                signal.signal(signum, self.handle)

    def handle(self, signum, frame):
        self.exitCode = const.INVALID_EXIT + signum
        msg = "Received signal %s: '%s'; exiting with code %s" % (
            signum, const.signalLookup[signum], self.exitCode)
        # XXX do a terminal write here
        print "\n" + msg
        log = registry.getLogger()
        log.msg(msg)
        sys.exit(self.exitCode)
