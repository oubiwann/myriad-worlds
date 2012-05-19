import sys

from twisted.application import service, internet
from twisted.python import usage

from dreamssh.sdk import scripts

from myriad import config, const, exceptions, meta
from myriad.game.service import getShellFactory


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
        ['game-type', 't', const.LOCAL,
         'The type of game to run; valid options incude: ,'.join(
            legalGameTypes)], 
        ['story-file', 's', '',
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
        interpreterType = self.get(const.INTERPRETER)
        if interpreterType and interpreterType not in self.legalInterpreters:
            raise exceptions.UnsupportedInterpreterType()
        if self.subCommand == const.KEYGEN:
            scripts.KeyGen()
            sys.exit(0)
        elif self.subCommand == const.SHELL:
            scripts.ConnectToShell()
            sys.exit(0)
        elif self.subCommand == const.STOP:
            scripts.StopDaemon()
            sys.exit(0)


def makeService(options):
    """
    """
    interpreterType = options.get(const.INTERPRETER)
    # primary setup
    application = service.Application(meta.description)
    services = service.IServiceCollection(application)
    # setup ssh access to a Python shell
    sshFactory = getShellFactory(
        interpreterType, app=application, services=services)
    sshserver = internet.TCPServer(config.ssh.port, sshFactory)
    sshserver.setName(config.ssh.servicename)
    sshserver.setServiceParent(services)
    return services
