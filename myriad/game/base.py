import imp, sys

from dreamssh.sdk import interfaces, registry

from myriad import util
from myriad.game.session import Session
from myriad.game.shell.grammar import ShellParser
from myriad.story import Story


config = registry.getConfig()


class Game(object):
    """
    """
    def __init__(self, name=""):
        self.name = name
        self.session = Session(name, game=self)
        self.story = None
        self.parser = None
        self.player = None

    def setUpStory(self):
        sys.path.insert(0, config.game.storydir)
        moduleData = imp.find_module(
            config.game.storymodule, [config.game.storydir])
        module = imp.load_module(config.game.storymodule, *moduleData)
        self.story = Story(config.game.storyfile)
        module.customizeItems(self.story)

    def setUpPlayer(self):
        self.player = self.story.world.player
        self.player.story = self.story

    def start(self):
        self.setUpStory()
        self.setUpPlayer()
        self.parser = ShellParser(session=self.session)

    def parseCommand(self, commandText):
        cmd = self.parser.parseCmd(commandText)
        #if isinstance(cmd, basestring):
        if cmd is not None:
            return cmd.command(self.player)

    def finish(self):
        # XXX do a terminal write here
        print
        print "You ended the game with:"
        for item in self.player.inv:
            print " -", util.aOrAn(item), item
        log = registry.getLogger()
        log.msg("Game has ended.")
