from ConfigParser import SafeConfigParser
import os

from zope.interface import moduleProvides

from dreamssh.config import Config, Configurator, main, ssh
from dreamssh.sdk import interfaces

from myriad import const, meta


moduleProvides(interfaces.IConfig)


# Main
main.config.userdir = os.path.expanduser("~/.%s" % meta.library_name)
main.config.userfile = "%s/%s" % (main.config.userdir, main.config.localfile)

# Internal SSH Server
ssh.servicename = meta.description
ssh.port = 4222
ssh.keydir = os.path.join(main.config.userdir, "ssh")
ssh.localdir = "~/.ssh"
ssh.banner = """:
: Welcome to
{{GAME_BANNER}}
:
:
: You have logged into a Myriad Worlds Server.
: {{HELP}}
:
: Enjoy!
:
"""

game = Config()
game.name = "The House II"
game.storydir = "examples/house-adventure-2"
game.storyfile = os.path.join(game.storydir, "story.yaml")
game.bannerfile = os.path.join(game.storydir, "banner.asc")
game.type = const.LOCAL


class MyriadConfigurator(Configurator):

    def __init__(self, main, ssh, game):
        super(MyriadConfigurator, self).__init__(main, ssh)
        self.game = game
        with open(game.bannerfile) as banner_file:
            self.ssh.banner.replace("{{GAME_BANNER}}", banner_file.read())

    def buildDefaults(self):
        config = super(MyriadConfigurator, self).buildDefaults()
        config.add_section("Game")
        config.set("Game", "name", self.game.name)
        config.set("Game", "storydir", self.game.storydir)
        config.set("Game", "storyfile", self.game.storyfile)
        config.set("Game", "bannerfile", self.game.bannerfile)
        config.set("Game", "type", self.game.type)
        return config

    def updateConfig(self):
        config = super(MyriadConfigurator, self).updateConfig()
        game = self.game
        # Game config
        #import pdb;pdb.set_trace()
        game.name = config.get("Game", "name")
        game.storydir = config.get("Game", "storydir")
        game.storyfile = config.get("Game", "storyfile")
        game.bannerfile = config.get("Game", "bannerfile")
        game.type = config.get("Game", "type")
        return config


configurator = MyriadConfigurator(main, ssh, game)
configurator.updateConfig()
