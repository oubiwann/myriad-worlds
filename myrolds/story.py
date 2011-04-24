import yaml

from myrolds.character import Player
from myrolds.map import Map
from myrolds.world import World
from myrolds.item import Item, OpenableItem


class Story(object):

    def __init__(self, filename):
        self.storyFile = filename
        self.stream = open(self.storyFile)
        self.data = yaml.load(self.stream)
        self.map = Map(self.data.get("map"))
        self.world = World()
        self.world.setScapes(self.map.getScapes())
        self.createItems()
        self.updateScapes()
        self.createCharacters()

    def _getItem(self, itemName):
        for item in self.data.get("items"):
            if item.get("name") == itemName:
                return item

    def getMap(self):
        return self.map.getData()

    def createItems(self):
        for itemData in self.data.get("items"):
            self.createItem(itemData)

    def updateScapes(self):
        scapesData = self.data.get("scapes")
        for scapeData in scapesData:
            scape = self.world.scapes.get(scapeData.get("room-key"))
            startingPlace = scapeData.get("startingPlace")
            if startingPlace:
                scape.startingPlace = True
                self.world.startingPlace = scape
            scape.name = scapeData.get("name")
            self.world.scapes[scape.name] = scape
            scape.desc = scapeData.get("description")
            scape.gameOver = scapeData.get("gameOver")
            itemsList = scapeData.get("items")
            if not itemsList:
                continue
            for itemName in itemsList:
                self.processItem(itemName, scape)

    def createItem(self, itemData):
        if itemData.get("isOpenable"):
            itemNames = itemData.pop("items")
            items = [Item.items[x] for x in itemNames]
            item = OpenableItem(itemData.get("name"), items)
        else:
            item = Item(**itemData)
        return item

    def processItem(self, itemName, scape):
        # XXX I don't like the way that all items are tracked on the Item
        # object... it doesn't make sense that every item in the world would
        # know about all other items in the world. Once that's fixed, we just
        # use the scape object's addItem method
        self.world.putItemInScape(itemName, scape)

    def createCharacters(self):
        for characterData in self.data.get("characters"):
            if characterData.get("isPlayer") == True:
                player = Player(characterData.get("name"))
                for itemName in characterData.get("inventory"):
                    player.take(Item.items[itemName])
                self.world.placeCharacterInScape(
                    player, self.world.startingPlace, isPlayer=True)
