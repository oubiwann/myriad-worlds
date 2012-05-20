from dreamssh.sdk import registry

from myriad import util
from myriad.game.session import Session
from myriad.game.shell.grammar import ShellParser


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
        print
        print "You ended the game with:"
        for item in self.player.inv:
            print " -", util.aOrAn(item), item
