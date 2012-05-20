import sys

from twisted.application import service, internet
from twisted.python import usage

from dreamssh.sdk import scripts

from myriad import config, const, meta
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
        [const.STORY_FILE, 's', '',
         'The path to the story.yaml file for the game.'],
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
        storyFile = self.get(const.STORY_FILE)
        print storyFile
        #if storyFile:
        # do the non-twisted subcommands
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
            import item_setup
            story = Story(config.game.storyfile)
            item_setup.customizeItems(story)
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
