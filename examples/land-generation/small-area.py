from myrolds.game import Game
from myrolds.story import Story


story = Story("examples/land-generation/small-area.yaml")
game = Game("save game 1")
game.play(story)
