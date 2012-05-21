from dreamssh.sdk import registry

from myriad import config


config.updateConfig()
registry.registerConfig(config)
