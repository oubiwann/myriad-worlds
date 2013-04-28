import inspect
import random

from myriad.world.base import Tile


class GeographicalFeature(Tile):
    desc = ""
    allowedTransitions = []
    allowedTransforms = {
        "increased temperature": [],
        "decreased temperature": [],
        }
    canHaveTown = True
    isPassable = True
    # human adult walking speed of 5 km/hr (83 m/min on flat, unencumbered
    # ground is taken as the unit speed.
    traversalMultiplier = 1.0


class Terrain(GeographicalFeature):
    pass


class WaterBody(GeographicalFeature):
    canHaveTown = False
    # comparing 5 km/hr (83 m/min) average walking time to average, casual
    # swimming speed of 3 km/hr (50 m/min)
    traversalMultiplier = 0.6


class Plains(Terrain):
    desc = "You are surrounded by grassy plains."
    pervasiveness = 0.8


class Savanna(Plains):
    desc = ("You are surrounded by grassland mixed with undergrowth and "
            "occasional trees.")


class Woodlands(Savanna):
    desc = "You are in an area of scattered woods and occasional clearings."
    traversalMultiplier = 0.6


class Forest(Woodlands):
    desc = "You are surrounded by trees."
    traversalMultiplier = 0.4


class Jungle(Forest):
    desc = "Wild vegetation lays before you, daunting in its thickness."
    traversalMultiplier = 0.1


class SandyGround(Plains):
    desc = "You are surrounded by sandy ground."
    traversalMultiplier = 0.6
    pervasiveness = 0.3


class RockyGround(Plains):
    desc = "You are surrounded by rocky ground."
    traversalMultiplier = 0.8
    pervasiveness = 0.3


class Hills(RockyGround):
    desc = "You have entered a hilly area."
    traversalMultiplier = 0.6
    pervasiveness = 0.5


class Cliffs(Hills):
    desc = "You face a wall of stone, a cliff too hight to pass unaided."
    isPassable = False
    pervasiveness = 0.3


class Caves(Hills):
    desc = "You are in an area with caves in the hills."
    traversalMultiplier = 0.5
    pervasiveness = 0.2


class Mountains(Hills):
    desc = "You are in the mountains"
    traversalMultiplier = 0.4
    pervasiveness = 0.4


class AlpineTreeline(Mountains):
    desc = ("You are in the mountains, below the treeline. You see the "
            "occasional Krummholz formation.")


class HighPeaks(Mountains):
    desc = ("The wind is blowing hard, and you have a difficult time "
            "breathing. You are very high up in the mountains, among "
            "the highest peaks.")
    traversalMultiplier = 0.1
    isPassable = False
    pervasiveness = 0.2


class HighPlateau(Mountains):
    desc = ("The wind is blowing hard, and you have a difficult time "
            "breathing. You are very high up in the mountains, on a "
            "large, moderately flat plateau. It is a forbidding environment.")
    traversalMultiplier = 0.7
    pervasiveness = 0.1


class Valley(Plains):
    desc = "Nestled between the slopes, you are standing in a valley."
    pervasiveness = 0.3


class Ravine(RockyGround):
    desc = ("You've managed to get yourself into a ravine. Let's see if you "
            "can get yourself out.")
    traversalMultiplier = 0.6
    isPassable = True
    pervasiveness = 0.3


class Canyon(Ravine):
    desc = ("You are now in a canyon. A most unenviable position for a "
            "traveller to be in.")
    isPassable = False
    pervasiveness = 0.3


class Desert(SandyGround):
    desc = ("You have entered the desert. You wonder how long your water "
            "will last if you have to keep this up...")
    traversalMultiplier = 0.4
    isPassable = False
    pervasiveness = 0.7


class Buttes(Desert, Hills):
    desc = "Several stunning buttes are within view."
    pervasiveness = 0.1


class Tundra(Desert):
    desc = "As far as you can see in that direction is a frozen wasteland."


class Shoreline(RockyGround):
    desc = ("You are at the water's edge. The rocky shore might be "
            "uncomfortable in barefeet.")
    pervasiveness = 0.4


class Beach(SandyGround):
    desc = ("You are on a beach. This would be a lovely place for a vacation. "
            "If you knew what vacations were.")
    pervasiveness = 0.3


class Stream(WaterBody):
    desc = "You are up to your needs in a stream."
    pervasiveness = 0.9


class River(Stream):
    desc = "For some reason, you've decided to take a swim in a river."
    isPassable = False


class Lake(WaterBody):
    desc = "You are currently in a lake."
    isPassable = False
    pervasiveness = 0.8


class Ocean(WaterBody):
    desc = "You have entered the ocean."
    isPassable = False
    pervasiveness = 0.9


# for procedural generation of tile layouts, valid transitions from one tile
# type to another have to be defined.
transitions = {
    Plains: [Plains, SandyGround, RockyGround, Hills, Valley, Desert, Beach,
             Canyon, River, Lake, Ocean, Jungle],
    Woodlands: [Plains, SandyGround, RockyGround, Hills, Valley, Beach,
                Woodlands, Forest, Jungle],
    Hills: [Plains, SandyGround, RockyGround, Hills, Mountains, Canyon, River,
           Lake],
    Mountains: [Hills, Mountains, HighPlateau, HighPeaks, Valley,
                AlpineTreeline],
    AlpineTreeline: [Mountains, HighPlateau, HighPeaks],
    HighPlateau: [Mountains, HighPlateau, HighPeaks, AlpineTreeline],
    Valley: [Plains, SandyGround, RockyGround, Hills, Mountains, River, Lake],
    Ravine: [Plains, SandyGround, RockyGround, Hills, Ravine, Canyon, River],
    Desert: [Plains, SandyGround, RockyGround, Ravine, Desert, Beach, Canyon,
             River, Lake, Ocean],
    Stream: [Shoreline, River, Stream, Lake],
    Lake: [Plains, SandyGround, RockyGround, Hills, Valley, Desert, Beach,
           River, Lake],
    Ocean: [Shoreline, River, Beach],
    Shoreline: [Ocean, Lake, River, Stream, Shoreline, Beach],
    }


transitions[Lake] = transitions[Stream]
transitions[River] = transitions[Stream] + [Beach]
transitions[SandyGround] = transitions[Plains]
transitions[Savanna] = transitions[Plains] + [Savanna, Woodlands]
transitions[Forest] = transitions[Woodlands]
transitions[Jungle] = transitions[Woodlands]
transitions[RockyGround] = transitions[Plains]
transitions[HighPeaks] = transitions[HighPlateau]
transitions[Canyon] = transitions[Ravine]
transitions[Buttes] = transitions[Desert]
transitions[Beach] = transitions[Plains]

# some terrain types require
requires = {
    # each valley tile should be connected to at least two mountains (on each
    # side)
    Valley: [],
    # each river tile should be connected directly to two other river tiles
    River: [],
    # each mountain should have a very high likelihood of having hills as
    # neighbors
    Mountains: [],
    # a beach must have water at least one one side
    Beach: [],
    # A river should be *very* pervasive, but in only distinct directions
    # (primarily usually only two neighbors will have river tiles... sometimes
    # a river will branch, in which case there might be three neigbors (non
    # touching, in that case). Also, where rivers meet oceans, an adjoining
    # tile should be another river tile, to help comprise a river delta.
    River: [],
    }


# the transformation of one terrain type into another would be something that
# occurred with a permanent change (local or global) in temperature (e.g., a
# river turning into a dry ravine).
transforms ={}


def getTileClasses():
    from myriad.world import terrain
    classes = inspect.getmembers(terrain, inspect.isclass)
    terrainClasses = [klass for name, klass in classes
        if issubclass(klass, terrain.Terrain)
        and klass is not terrain.Terrain]
    waterClasses = [klass for name, klass in classes
        if issubclass(klass, terrain.WaterBody)
        and klass is not terrain.WaterBody]
    return terrainClasses + waterClasses


def getRandomTileClass():
    # XXX this needs to use the session randomizer... need to move this
    return random.choice(getTileClasses())


def getPassableRandomTileClass():
    tile = getRandomTileClass()
    while not tile.isPassable:
        tile = getRandomTileClass()
    return tile


def getRandomTileTransitionClass(tile, neighborTiles):
    # build sets of all valid transitions for each neighbor, then to find a
    # transition that's valid for them all simultaneously, do an intersection
    if not neighborTiles:
        intersections = transitions[tile]
    elif len(neighborTiles) == 1:
        intersections = neighborTiles
    else:
        intersections = []
        for index, tile in enumerate(neighborTiles):
            if index == len(neighborTiles) - 1:
                break
            thisTransition = transitions[tile]
            nextTransition = transitions[neighborTiles[index + 1]]
            intersections.extend(
                list(set(thisTransition).intersection(nextTransition)))
        # remove redundancies
        intersections = list(set(intersections))
    # the higher tendency the tile is to be pervasive, the more likely the
    # tile will continue being used; if the same tile is not pervaded, randomly
    # select a valid transition tile from the intersections

    # XXX this needs to use the session randomizer... need to move this
    reuseCheck = random.random()
    if tile in intersections and reuseCheck < tile.pervasiveness:
        return tile

    # XXX this needs to use the session randomizer... need to move this
    return random.choice(intersections)
