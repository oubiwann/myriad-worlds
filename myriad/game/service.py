import os, sys

from twisted.application import service, internet
from twisted.python import log, usage

from dreamssh.sdk import interfaces, registry, scripts

from myriad import const, meta, util
from myriad.game import runner
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
        [const.STORY_DIR, 'd', './examples/house-adventure-2',
         'The path to the directory that holds the game data.'],
        [const.STORY_FILE, 'f', 'story.yaml',
         'The filename of the story (YAML) file.'],
        [const.STORY_MODULE, 'm', 'item_setup',
         'The filename of the Python module that does game pre-processing.'],
        [const.BANNER_FILE, 'b', 'banner.asc',
         'The filename of the login banner.'],
        [const.LOG_FILE, 'l', 'game.log',
         'The file to which log messages should be sent.'],
        ]
    subCommands = [
        [const.KEYGEN, None, SubCommandOptions,
         "Generate ssh keys for the server"],
        [const.SHELL, None, SubCommandOptions, "Login to the server"],
        [const.STOP, None, SubCommandOptions, "Stop the server"],
        ]

    def parseOptions(self, options):
        config = registry.getConfig()
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
        if not storyDir == config.game.storydir:
            config.game.storydir = storyDir
            config.game.storyfile = os.path.abspath(os.path.join(
                storyDir, storyFile))
            config.game.storymodule = storyModule
            with open(bannerFile) as bannerFile:
                config.game.banner = util.renderBanner(
                    config.ssh.banner, bannerFile.read(),
                    config.game.helpprompt)
        if self.subCommand == const.KEYGEN:
            scripts.KeyGen()
            sys.exit(const.OK)
        elif self.subCommand == const.SHELL:
            scripts.ConnectToShell()
            sys.exit(const.OK)
        elif self.subCommand == const.STOP:
            scripts.StopDaemon()
            sys.exit(const.OK)
        # do the non-twisted game types
        if gameType == const.LOCAL:
            util.setupLogging(self.get(const.LOG_FILE))
            runner.runLocal()


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
