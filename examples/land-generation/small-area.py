from myriad.game import Game
from myriad.story import Story


story = Story("examples/land-generation/small-area.yaml")
game = Game("save game 1")
game.play(story)
