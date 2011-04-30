from myrolds.game import Game
from myrolds.item import Item, OpenableItem
from myrolds.story import Story


# start game definition
story = Story("examples/house-adventure/story.yaml")


# programmatic item customizations
# XXX do we want to do this here? or in YAML, similar to what Inform 7 does?
Item.items["shovel"].usableConditionTest = (
    lambda player, target: player.room is story.world.getScape("garden"))
def useShovel(player, subj, target):
    coin = Item.items["coin"]
    if not coin.isVisible and coin in player.room.inv:
        coin.isVisible = True
Item.items["shovel"].useAction = useShovel

Item.items["telescope"].usableConditionTest = lambda player, target: True
def useTelescope(player, subj, target):
    print "You don't see anything."
Item.items["telescope"].useAction = useTelescope


# start game
game = Game("House Adventure")
game.play(story)
