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


class SandyGround(Plains):
    traversalMultiplier = 0.8


class RockyGround(Plains):
    defaultDesc = ""


class Hills(RockyGround):
    defaultDesc = ""
    traversalMultiplier = 0.6


class Mountains(Hills):
    defaultDesc = ""
    traversalMultiplier = 0.4


class HighPeaks(Mountain):
    defaultDesc = ""
    traversalMultiplier = 0.1


class HighPlateau(Mountain):
    defaultDesc = ""


class Valley(Plains):
    defaultDesc = ""


class Desert(SandyGround):
    defaultDesc = ""


class Beach(SandyGround):
    defaultDesc = ""


class Ravine(Terrain):
    defaultDesc = ""


class Canyon(Ravine):
    defaultDesc = ""


class Cave(RockyGround):
    defaultDesc = ""


class River(WaterBody):
    defaultDesc = ""


class Lake(WaterBody):
    defaultDesc = ""


class Ocean(WaterBody):
    defaultDesc = ""


# for procedural generation of tile layouts, valid transitions from one tile
# type to another have to be defined.
transitions = {
    Plains: [SandyGround, RockyGround, Hills, Valley, Desert, Beach, Canyon,
             Cave, River, Lake, Ocean],
    Hills: [Plains, SandyGround, RockyGround, Hills, Mountains, Canyon, Cave,
            River, Lake],
    Mountains: [Hills, Mountains, HighPlateau, HighPeaks, Valley, Cave],
    Highlateau: [Mountains, HighPlateau, HighPeaks],
    Valley: [Plains, SandyGround, RockyGround, Hills, Mountains, River, Lake,
             Ocean],
    Ravine: [Plains, SandyGround, RockyGround, Hills, Ravine, Canyon, Cave,
             River],
    Cave: [Plains, SandyGround, RockyGround, Hills, Mountains, HighPlateau,
           HighPeaks, Desert, Canyon, Valley],
    River: [Plains, SandyGround, RockyGround, Hills, Desert, Beach, Canyon,
            Cave, River, Lake, Ocean],
    Lake: [],
    Ocean: [],
    }


transitions[SandyGround] = transitions[Plains]
transitions[RockyGround] = transitions[Plains]
transitions[HighPeaks] = transitions[HighPlateau]
transitions[Canyon] = transitions[Ravine]
transitions[Desert] = transitions[Plains]
transitions[Beach] = transitions[Plains]


# the transformation of one terrain type into another would be something that
# occurred with a permanent change (local or global) in temperature (e.g., a
# river turning into a dry ravine).
transforms ={}
