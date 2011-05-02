from myrolds import util
from myrolds.game.session import Session
from myrolds.game.shell import ShellParser


class Game(object):

    def __init__(self, name=""):
        self.name = name
        self.session = Session(name, game=self)
        self.story = None
        self.parser = None
        self.player = None

    def play(self, story=None):
        if story:
            self.story = story
        self.player = story.world.player
        # create parser
        self.parser = ShellParser(session=self.session)
        self.mainLoop()
        self.finish()

    def mainLoop(self):
        while not self.player.gameOver:
            cmdstr = raw_input(">> ")
            cmd = self.parser.parseCmd(cmdstr)
            if cmd is not None:
                cmd.command(self.player)

    def finish(self):
        print
        print "You ended the game with:"
        for item in self.player.inv:
            print " -", util.aOrAn(item), item
