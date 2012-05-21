import imp, sys

from dreamssh.sdk import interfaces, registry

from myriad import const, util
from myriad.game.session import Session
from myriad.game.shell.grammar import ShellParser
from myriad.story import Story


config = registry.getConfig()


class LocalGame(object):

    def __init__(self, name=""):
        self.name = name
        self.session = Session(name, game=self)
        self.story = None
        self.parser = None
        self.player = None
        self.startedLoop = False

    def play(self, story=None):
        if story:
            self.story = story
        self.player = story.world.player
        self.player.story = story
        # create parser
        self.parser = ShellParser(session=self.session)
        self.mainLoop()
        self.finish()

    def mainLoop(self):
        prompt = config.game.banner
        while not self.player.gameOver:
            if not self.startedLoop:
                prompt += ">> "
            else:
                prompt = ":>> "
            cmdstr = raw_input(prompt)
            self.startedLoop = True
            cmd = self.parser.parseCmd(cmdstr)
            if cmd is not None:
                cmd.command(self.player)

    def finish(self):
        # XXX do a terminal write here
        print
        print "You ended the game with:"
        for item in self.player.inv:
            print " -", util.aOrAn(item), item


def runLocal():
    log = registry.getLogger()
    log.msg("Starting local (non-service) game ...")
    sys.path.insert(0, config.game.storydir)
    moduleData = imp.find_module(
        config.game.storymodule, [config.game.storydir])
    module = imp.load_module(config.game.storymodule, *moduleData)
    story = Story(config.game.storyfile)
    module.customizeItems(story)
    handler = util.SignalHandler()
    game = LocalGame()
    try:
        game.play(story)
    except EOFError, e:
        if handler.exitCode == const.OK:
            handler.exitCode = const.CONTROL_D
            msg = "Received ^D; exiting ..."
            # XXX do a terminal write here
            print "\n" + msg
            log.msg(msg)
    sys.exit(handler.exitCode)
