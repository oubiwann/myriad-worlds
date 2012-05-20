from myriad.item import Item, OpenableItem


def customizeItems(story):
    # programmatic item customizations
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


    Item.items["sign"].isTakeable = False
    Item.items["sign"].readableConditionTest = (
        lambda player, target: target in player.room.inv)
    def readSign(p, subj, target):
        if Item.items["magnifying glass"] in p.inv:
            print ("The sign says in very tiny writing 'Danger! Quicksand!', "
                   "and there is a little teeny arrow pointing, um, west.")
        else:
            print "There is writing on the sign, but it is too small to read."
    Item.items["sign"].readAction = readSign
