import sys
import os

from twisted.application import service, internet
from twisted.python import usage

from dreamssh.sdk import registry, scripts

from myriad import const, meta, util
from myriad.game.shell.service import getShellFactory




class SubCommandOptions(usage.Options):
    """
    A base class for subcommand options.

    Can also be used directly for subcommands that don't have options.
    """


class Options(usage.Options):
    """
    """
    legalGameTypes = [const.LOCAL, const.SINGLE, const.MULTI]
    optParameters = [
        [const.GAME_TYPE, 't', const.LOCAL,
         'The type of game to run; valid options incude: ' + 
         ', '.join(legalGameTypes)], 
        [const.STORY_FILE, 'f', 'story.yaml',
         'The filename of the story (YAML) file.'],
        [const.STORY_MODULE, 'm', 'item_setup',
         'The filename of the Python module that does game pre-processing.'],
        [const.BANNER_FILE, 'b', 'banner.asc',
         'The filename of the login banner.'],
        [const.STORY_DIR, 'd', '',
         'The path to the directory that holds the game data.'],
        ]
    subCommands = [
        [const.KEYGEN, None, SubCommandOptions,
         "Generate ssh keys for the server"],
        [const.SHELL, None, SubCommandOptions, "Login to the server"],
        [const.STOP, None, SubCommandOptions, "Stop the server"],
        ]

    def parseOptions(self, options):
        usage.Options.parseOptions(self, options)
        # check options
        gameType = self.get(const.GAME_TYPE)
        if gameType and gameType not in self.legalGameTypes:
            msg = "'%s' is not a supported game type'" % gameType
            raise exceptions.UnsupportedGameType(msg)
        storyDir = self.get(const.STORY_DIR)
        storyFile = self.get(const.STORY_FILE)
        storyModule = self.get(const.STORY_MODULE)
        bannerFile = os.path.abspath(os.path.join(
            storyDir, self.get(const.BANNER_FILE)))
        config = registry.getConfig()
        if not storyDir == config.game.storydir:
            config.game.storydir = storyDir
            config.game.storyfile = os.path.abspath(os.path.join(
                storyDir, storyFile))
            config.game.storymodule = storyModule
            with open(bannerFile) as bannerFile:
                config.game.banner = util.renderBanner(
                    config.ssh.banner, bannerFile.read(), config.game.helpprompt)
        if self.subCommand == const.KEYGEN:
            scripts.KeyGen()
            sys.exit(0)
        elif self.subCommand == const.SHELL:
            scripts.ConnectToShell()
            sys.exit(0)
        elif self.subCommand == const.STOP:
            scripts.StopDaemon()
            sys.exit(0)
        # do the non-twisted game types
        if gameType == const.LOCAL:
            from myriad.game.runner import LocalGame
            from myriad.story import Story
            sys.path.insert(0, config.game.storydir)
            import imp
            moduleData = imp.find_module(
                config.game.storymodule, [config.game.storydir])
            module = imp.load_module(config.game.storymodule, *moduleData)
            story = Story(config.game.storyfile)
            module.customizeItems(story)
            game = LocalGame()
            game.play(story)
            sys.exit(0)


def makeService(options):
    """
    """
    # primary setup
    application = service.Application(meta.description)
    services = service.IServiceCollection(application)
    # setup ssh access to a Python shell
    sshFactory = getShellFactory(
        app=application, services=services)
    sshserver = internet.TCPServer(config.ssh.port, sshFactory)
    sshserver.setName(config.ssh.servicename)
    sshserver.setServiceParent(services)
    return services
