import inspect
import itertools
import random

from myrolds.const import N, S, E, W, NE, NW, SE, SW, C
from myrolds.data import terrain


def aOrAn(item):
    if item.desc[0] in "aeiou":
        return "an"
    else:
        return "a"


def enumerateItems(items):
    if len(items) == 0:
        return "nothing"
    out = []
    for item in items:
        if len(items) > 1 and item == items[-1]:
            out.append("and")
        out.append(aOrAn(item))
        if item == items[-1]:
            out.append(item.desc)
        else:
            if len(items) > 2:
                out.append(item.desc + ",")
            else:
                out.append(item.desc)
    return " ".join(out)


def enumerateExits(l):
    if len(l) == 0: return ""
    out = []
    for item in l:
        if len(l) > 1 and item == l[-1]:
            out.append("and")
        if item == l[-1]:
            out.append(item)
        else:
            if len(l) > 2:
                out.append(item + ",")
            else:
                out.append(item)
    return " ".join(out)


def getRandomInts(min=0, max=1, step=1, count=1):
    max += step
    # XXX this needs to use the session randomizer... need to move this
    # function into a class that the session can get access to (the session has
    # access to the game, and thus the story, world, and player objects...
    # world has access to map objects, so that seems like a good place)
    return [random.randrange(min, max, step) for x in xrange(count)]


def getTileClasses():
    from myrolds.data import terrain
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
        intersections = terrain.transitions[tile]
    elif len(neighborTiles) == 1:
        intersections = neighborTiles
    else:
        intersections = []
        for index, tile in enumerate(neighborTiles):
            if index == len(neighborTiles) - 1:
                break
            thisTransition = terrain.transitions[tile]
            nextTransition = terrain.transitions[neighborTiles[index + 1]]
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
    return choice


def createEmptyGrid(x, y):
    return [[0] * x for j in xrange(y)]


def getSurroundingIndices(x, y, grid):
    """"
    Each tile will have 8 surrounding tiles, 4 for the 4 cardinal directions
    (n, s, e, w), and 4 for the intermediate directions (nw, ne, se, sw). Tiles
    at the edge will only wrap if 
    """
    maxXIndex = len(grid[0]) - 1
    maxYIndex = len(grid) - 1
    indices = {
        C: (x, y),
        NW: (x - 1, y - 1),
        N: (x, y - 1),
        NE: (x + 1, y - 1),
        E: (x + 1, y),
        SE: (x + 1, y + 1),
        S: (x, y + 1),
        SW: (x - 1, y + 1),
        W: (x - 1, y),
        }
    for direction, value in indices.items():
        if (-1 in value) or (value[0] > maxXIndex) or (value[1] > maxYIndex):
            indices[direction] = None
    return indices


def setSurroundingTiles(tile, x, y, grid):
    """
    For each random tile we select, we need to 1) make sure that its a valid
    transition from all surrounding tiles, and 2) make sure that there are
    least two passable neighboring tiles.
    """
    neighbors = getSurroundingIndices(x, y, grid)
    neighborClasses = []
    emptyTiles = []
    for direction, coords in neighbors.items():
        # if the neighbor is off the grid (e.g., tile would be on the border),
        # skip it
        if not coords:
            continue
        (neighborX, neighborY) = coords
        neighborTile = grid[neighborY][neighborX]
        # let's track the tiles that need to be set
        if neighborTile == 0:
            emptyTiles.append((neighborX, neighborY))
        # let's separately track the tiles that have already been set
        elif issubclass(neighborTile, terrain.GeographicalFeature):
            neighborClasses.append(neighborTile)
        else:
            raise Exception("What *is* this tile?!?")
    for x, y in emptyTiles:
        grid[y][x] = getRandomTileTransitionClass(tile, neighborClasses)
    # once all the neighbors have been set, get the next unset (x, y) and
    # re-run; we'll use the eastern-most neighbor until we run out of tiles in
    # the current row
    neighbor = neighbors[E]
    if neighbor:
        newX, newY = neighbors[E]
    else:
        newX, newY = (0, y + 1)
    # this next checks for y values that are off the grid (which indicates that
    # we're done)
    if newY > len(grid):
        return
    # this collapses all the rows into a single array; if all the zeros have
    # been replaced with terrain classes, we're done
    if 0 not in itertools.chain(*grid):
        return
    setSurroundingTiles(grid[newY][newX], newX, newY, grid)


def setGridBoundaries(grid):
    """
    Set all boundary tiles as non-passable in off-grid directions.

    Grids that represent a blog (e.g., planetary sized grids) should not use
    this methods; those grids should instead wrap at their boundaries.
    """
    # set top tiles as unpassable in the N direction
    # set bottom tiles as unpassable in the S direction
    # set right tiles as unpassable in the E direction
    # set left tiles as unpassable in the W direction
