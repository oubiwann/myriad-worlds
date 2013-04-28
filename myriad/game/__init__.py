from carapace.sdk import registry

from myriad import config


config.updateConfig()
registry.registerConfig(config)
