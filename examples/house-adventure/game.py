from pyparsing import *
import random


#====================
# start game definition
roomMap = open("map.asc").read()
rooms = createRooms(roomMap)
rooms["A"].desc = "You are standing at the front door."
rooms["b"].desc = "You are in a garden."
rooms["c"].desc = "You are in a kitchen."
rooms["d"].desc = "You are on the back porch."
rooms["e"].desc = "You are in a library."
rooms["f"].desc = "You are on the patio."
rooms["q"].desc = "You are sinking in quicksand.  You're dead..."
rooms["q"].gameOver = True

# define global variables for referencing rooms
frontPorch = rooms["A"]
garden     = rooms["b"]
kitchen    = rooms["c"]
backPorch  = rooms["d"]
library    = rooms["e"]
patio      = rooms["f"]

# create items
itemNames = """sword.diamond.apple.flower.coin.shovel.book.mirror.telescope.gold bar""".split(".")
for itemName in itemNames:
    Item( itemName )
Item.items["apple"].isDeadly = True
Item.items["mirror"].isFragile = True
Item.items["coin"].isVisible = False
Item.items["shovel"].usableConditionTest = ( lambda p,t: p.room is garden )

def useShovel(p,subj,target):
    coin = Item.items["coin"]
    if not coin.isVisible and coin in p.room.inv:
        coin.isVisible = True
Item.items["shovel"].useAction = useShovel

Item.items["telescope"].isTakeable = False

def useTelescope(p,subj,target):
    print "You don't see anything."

Item.items["telescope"].useAction = useTelescope

OpenableItem("treasure chest", Item.items["gold bar"])

putItemInRoom("shovel", frontPorch)
putItemInRoom("coin", garden)
putItemInRoom("flower", garden)
putItemInRoom("apple", library)
putItemInRoom("mirror", library)
putItemInRoom("telescope", library)
putItemInRoom("book", kitchen)
putItemInRoom("diamond", backPorch)
putItemInRoom("treasure chest", patio)

# create player
plyr = Player("Bob")
plyr.take( Item.items["sword"] )

# start game
playGame( plyr, frontPorch )
