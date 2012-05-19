from twisted.application.service import ServiceMaker


ExampleMyriadWorldService = ServiceMaker(
    "Myriad World Server",
    "myriad.game.service",
    "An example single-player SSH server for Myriad Worlds.",
    "myriad")
