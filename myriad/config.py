from ConfigParser import SafeConfigParser
import os

from zope.interface import moduleProvides

from dreamssh.sdk import interfaces

from myriad import meta


moduleProvides(interfaces.IConfig)


# XXX move this into dreamssh.common
class Config(object):
    pass


# Main
main = Config()
main.config = Config()
main.config.userdir = os.path.expanduser("~/.%s" % meta.library_name)
main.config.localfile = "config.ini"
main.config.userfile = "%s/%s" % (main.config.userdir, main.config.localfile)

# Internal SSH Server
ssh = Config()
ssh.servicename = meta.description
ssh.port = 4222
ssh.pidfile = "twistd.pid"
ssh.username = "root"
ssh.keydir = os.path.join(main.config.userdir, "ssh")
ssh.privkey = "id_rsa"
ssh.pubkey = "id_rsa.pub"
ssh.localdir = "~/.ssh"
ssh.banner = """:
: Welcome to
:
:________                              ____________________  __
:___  __ \_________________ _______ _____  ___/_  ___/__  / / /
:__  / / /_  ___/  _ \  __ `/_  __ `__ \____ \_____ \__  /_/ /
:_  /_/ /_  /   /  __/ /_/ /_  / / / / /___/ /____/ /_  __  /
:/_____/ /_/    \___/\__,_/ /_/ /_/ /_//____/ /____/ /_/ /_/
:
:
: You have logged into a Myriad Worlds Server.
: {{HELP}}
:
: Enjoy!
:
"""

game = Config()
game.name = "The House"
game.dir = "examples/house-adventure-2/"
# XXX buildDefaults will need to set these
# XXX updateConfig will need to set these

# XXX move this into dreamssh.util
def buildDefaults():
    config = SafeConfigParser()
    config.add_section("SSH")
    config.set("SSH", "servicename", ssh.servicename)
    config.set("SSH", "port", str(ssh.port))
    config.set("SSH", "pidfile", ssh.pidfile)
    config.set("SSH", "username", ssh.username)
    config.set("SSH", "keydir", ssh.keydir)
    config.set("SSH", "privkey", ssh.privkey)
    config.set("SSH", "pubkey", ssh.pubkey)
    config.set("SSH", "localdir", ssh.localdir)
    config.set("SSH", "banner", ssh.banner)
    return config

# XXX move this into dreamssh.util
def getConfigFile():
    if os.path.exists(main.config.localfile):
        return main.config.localfile
    if not os.path.exists(main.config.userdir):
        os.mkdir(os.path.expanduser(main.config.userdir))
    return main.config.userfile


# XXX move this into dreamssh.util
def writeDefaults():
    config = buildDefaults()
    with open(getConfigFile(), "wb") as configFile:
        config.write(configFile)


# XXX move this into dreamssh.util
def updateConfig():
    config = SafeConfigParser()
    config.read(getConfigFile())

    # Internal SSH Server
    ssh.servicename = config.get("SSH", "servicename")
    ssh.port = int(config.get("SSH", "port"))
    ssh.pidfile = config.get("SSH", "pidfile")
    ssh.username = str(config.get("SSH", "username"))
    ssh.keydir = config.get("SSH", "keydir")
    ssh.privkey = config.get("SSH", "privkey")
    ssh.pubkey = config.get("SSH", "pubkey")
    ssh.localdir = config.get("SSH", "localdir")
    ssh.banner = str(config.get("SSH", "banner"))


configFile = getConfigFile()
if not os.path.exists(configFile):
    writeDefaults()
updateConfig()


del Config
del configFile, updateConfig
