import random

from myrolds import util


class Session(object):
    """
    The Session object is intended for game-specific data and metadata that
    doesn't belong in the game world or story.
    """
    def __init__(self, name, game=None):
        """
        The "name" parameter should be the game name. It will be used for
        saving session data and seeding the randomizer.
        """
        self.name = name
        self.randomizer = None
        self.game = game

    def getRandomizer(self):
        """
        We want the ability to provide randomly-generated environments, while
        at the same time allowing users to return to the same world, once
        generated.  This can be accomplished by using the same seed when
        creating an instance of the Random object. 

        This utility function is a convenience, as it sets everything up for
        the developer.
        """
        if not self.randomizer:
            randomizer = random.Random()
            randomizer.seed(self.seed)
            self.randomizer = randomizer
        return self.randomizer

    def save(self):
        pass

    def load(self):
        pass
