import imp, sys

from dreamssh.sdk import interfaces, registry

from myriad import const, util
from myriad.game import base
from myriad.game.session import Session


config = registry.getConfig()


class LocalGame(base.Game):

    def __init__(self, name=""):
        super(LocalGame, self).__init__(name=name)
        self.startedLoop = False

    def start(self):
        super(LocalGame, self).start()
        self.mainLoop()
        self.finish()

    def mainLoop(self):
        prompt = config.game.banner
        while not self.player.gameOver:
            if not self.startedLoop:
                prompt += ">> "
                self.startedLoop = True
            else:
                prompt = ":>> "
            self.parseCommand(raw_input(prompt))


def runLocal():
    log = registry.getLogger()
    log.msg("Starting local (non-service) game ...")
    handler = util.SignalHandler()
    game = LocalGame()
    try:
        game.start()
    except EOFError, e:
        if handler.exitCode == const.OK:
            handler.exitCode = const.CONTROL_D
            msg = "Received ^D; exiting ..."
            # XXX do a terminal write here
            print "\n" + msg
            log.msg(msg)
    sys.exit(handler.exitCode)
