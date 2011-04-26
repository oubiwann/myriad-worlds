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


class Valley(Plains):
    defaultDesc = ""


class HighPeaks(Mountain):
    defaultDesc = ""
    traversalMultiplier = 0.1


class Desert(SandyGround):
    defaultDesc = ""


class Beach(SandyGround):
    defaultDesc = ""


class Canyon(Terrain):
    defaultDesc = ""


class Cave(RockyGround):
    defaultDesc = ""


class River(WaterBody):
    defaultDesc = ""


class Lake(WaterBody):
    defaultDesc = ""


class Ocean(WaterBody):
    defaultDesc = ""
