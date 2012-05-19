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
    legalInterpreters = [const.PYTHON, const.ECHO]
    optParameters = [
        ["interpreter", "i", "python",
         ("The interpreter to use; valid options incude: "
          ",".join(legalInterpreters))]
         ]
    subCommands = [
        ["keygen", None, SubCommandOptions,
         "Generate ssh keys for the server"],
        ["shell", None, SubCommandOptions, "Login to the server"],
        ["stop", None, SubCommandOptions, "Stop the server"],
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
