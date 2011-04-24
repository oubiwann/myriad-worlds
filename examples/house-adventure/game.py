from myrolds import shell
from myrolds.item import Item, OpenableItem
from myrolds.story import Story
from myrolds.world import World


# start game definition
story = Story("examples/house-adventure/story.yaml")


# programmatic item customizations
Item.items["shovel"].usableConditionTest = (
    lambda player, target: p.room is garden)
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
shell.playGame(story)
