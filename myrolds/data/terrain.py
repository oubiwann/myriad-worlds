class GeographicalFeature(object):
    defaultDesc = ""
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
    defaultDesc = ""
    isPassable = True
    pervasiveness = 0.8


class SandyGround(Plains):
    traversalMultiplier = 0.8
    isPassable = True
    pervasiveness = 0.3


class RockyGround(Plains):
    defaultDesc = ""
    isPassable = True
    pervasiveness = 0.3


class Hills(RockyGround):
    defaultDesc = ""
    traversalMultiplier = 0.6
    isPassable = True
    pervasiveness = 0.5


class Mountains(Hills):
    defaultDesc = ""
    traversalMultiplier = 0.4
    isPassable = True
    pervasiveness = 0.4


class HighPeaks(Mountains):
    defaultDesc = ""
    traversalMultiplier = 0.1
    isPassable = False
    pervasiveness = 0.2


class HighPlateau(Mountains):
    defaultDesc = ""
    isPassable = True
    pervasiveness = 0.1


class Valley(Plains):
    defaultDesc = ""
    isPassable = True
    pervasiveness = 0.3


class Desert(SandyGround):
    defaultDesc = ""
    isPassable = False
    pervasiveness = 0.7


class Beach(SandyGround):
    defaultDesc = ""
    isPassable = True
    pervasiveness = 0.3


class Ravine(Terrain):
    defaultDesc = ""
    isPassable = True
    pervasiveness = 0.3


class Canyon(Ravine):
    defaultDesc = ""
    isPassable = False
    pervasiveness = 0.3


class River(WaterBody):
    defaultDesc = ""
    isPassable = False
    pervasiveness = 0.3


class Lake(WaterBody):
    defaultDesc = ""
    isPassable = False
    pervasiveness = 0.7


class Ocean(WaterBody):
    defaultDesc = ""
    isPassable = False
    pervasiveness = 0.9

# for procedural generation of tile layouts, valid transitions from one tile
# type to another have to be defined.
transitions = {
    Plains: [Plains, SandyGround, RockyGround, Hills, Valley, Desert, Beach,
             Canyon, River, Lake, Ocean],
    Hills: [Plains, SandyGround, RockyGround, Hills, Mountains, Canyon, River,
           Lake],
    Mountains: [Hills, Mountains, HighPlateau, HighPeaks, Valley],
    HighPlateau: [Mountains, HighPlateau, HighPeaks],
    Valley: [Plains, SandyGround, RockyGround, Hills, Mountains, River, Lake],
    Ravine: [Plains, SandyGround, RockyGround, Hills, Ravine, Canyon, River],
    Desert: [Plains, SandyGround, RockyGround, Ravine, Desert, Beach, Canyon,
             River, Lake, Ocean],
    River: [Plains, SandyGround, RockyGround, Hills, Desert, Beach, Canyon,
            River, Lake, Ocean],
    Lake: [Plains, SandyGround, RockyGround, Hills, Valley, Desert, Beach,
           River, Lake],
    Ocean: [Plains, SandyGround, RockyGround, Hills, Desert, Beach, River],
    }


transitions[SandyGround] = transitions[Plains]
transitions[RockyGround] = transitions[Plains]
transitions[HighPeaks] = transitions[HighPlateau]
transitions[Canyon] = transitions[Ravine]
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
