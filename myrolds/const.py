# Human perceptual average distance to horizon on Earth, in miles; this is
# taken as the unit size of a tile. To provide some reference, a small town of
# 3000 people can easily fit in 2 square miles (that's about 1300 residential
# buildings). So a single tile of 3.1 miles x 3.1 miles will provide plenty of
# space for a small town.
# 
# A large city can be in the neighborhood of 500 square miles (e.g., New York
# City) with a population density of 28,000 people per square mile (which would
# be 84000 people per tile). A city the size of NYC would require about 150
# tiles, a grid of 10 by 15 tiles.
#
# The next step up in order of magnitude, 100 by 100 tiles, would be about the
# size of the state of Michigan (the 11th largest state in the US).
# 
# As a further extreme, a continent the size of North America (about 3 times
# larger than the surface area of Australia) would be 1000 by 1000 tiles.

# And finally, the Earth itself has a total of 316944047 square miles (land and
# sea) which would be about 102240015 tiles, or a grid of 10002 by 10222 tiles.
horizonDistance = 3.1

# directions
N = 0
S = 1
E = 2
W = 3
NE = 4
NW = 5
SE = 6
SW = 7
# the last one is "center"
C = 8
