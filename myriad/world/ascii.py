grey = '\033[90m'
red = '\033[91m'
green = '\033[92m'
yellow = '\033[93m'
blue = '\033[94m'
magenta = '\033[95m'
cyan = '\033[96m'
white = '\033[97m'
end_color = '\033[0m'

test_terrain = r"""%s
1234
abcd
56
e
%s
""" % ("noop", "noop")

plains = r"""%s
----
----
--
-
%s
""" % (yellow, end_color)

savanna = r"""%s
-+--
--+-
-+
-
%s
""" % (yellow, end_color)

woodlands = r"""%s
+-++
++-+
+-
+
%s
""" % (green, end_color)

forest = r"""%s
++++
++++
++
+
%s
""" % (green, end_color)

jungle = r"""%s
$+&+
+&+$
&+
&
%s
""" % (green, end_color)

sandy_ground = r"""%s
....
....
..
.
%s
""" % (yellow, end_color)

desert = sandy_ground
beach = sandy_ground

rocky_ground = r"""%s
,.,.
.,.,
,.
,
%s
""" % (grey, end_color)

shoreline = rocky_ground

hills = r"""%s
^_^_
_^_^
^_
^
%s
""" % (red, end_color)

cliffs = r"""%s
|,,.
.,,|
|,
|
%s
""" % (red, end_color)

caves = r"""%s
^_^_
_O_O
_O
o
%s
""" % (red, end_color)

mountains = r"""%s
^^^^
^^^^
^^
^
%s
""" % (red, end_color)

alpine_treeline = r"""%s
^+^+
+^+^
^+
^
%s
""" % (red, end_color)

high_peaks = r"""%s
/\**
**/\
^*
^
%s
""" % (white, end_color)

high_plateau = r"""%s
/\__
__/\
^_
^
%s
""" % (red, end_color)

valley = r"""%s
\/--
--\/
V-
v
%s
""" % (green, end_color)

ravine = r"""%s
-V-v
v-V- Ravine
V-
v
%s
""" % (red, end_color)

canyon = r"""%s
_  _
 \/
VV
V
%s
""" % (red, end_color)

buttes = r"""%s
...n
n...
n.
n
%s
""" % (red, end_color)

tundra = r"""%s
*.*.
.*.*
.*
*
%s
""" % (white, end_color)

stream = r"""%s
~S~s
s~S~
~s
~
%s
""" % (cyan, end_color)

river = r"""%s
~{~{
}~}~
~S
~
%s
""" % (cyan, end_color)

lake = r"""%s
~.~.
.~.~
~.
~
%s
""" % (blue, end_color)

ocean = r"""%s
~~~~
~~~~
~~
~
%s
""" % (blue, end_color)

"""
The following ASCII terrain snippets are either old or haven't been used yet.

^\/^
/^^\ Valley (old)

++++
++++

$&$&
&$&$

,.,.
.,., RockyGround (Shoreline)

....
.... SandyGround (Desert/Beach)

====
====

''''
''''

;;;;
;;;;

::::
::::

____
____
"""


large = (1, 3)
large_top = (1, 2)
large_bottom = (2, 3)
medium = (3, 4)
small = (4, 5)


def get_terrain(name, size=large, color=False):
    color_start = ""
    color_end = ""
    name_parts = name.splitlines()
    if color:
        color_start = name_parts[0]
        color_end = name_parts[-1]
    terrain = name_parts[size[0]:size[1]]
    if len(terrain) == 1:
        terrain = [color_start + terrain[0] + color_end]
    elif len(terrain) == 2:
        terrain = [color_start + terrain[0], terrain[1] + color_end]
    return terrain


def print_terrain(name, size=large, color=True):
    print "\n".join(get_terrain(name, size, color))


def get_terrain_row(names, size=large, color=False):
    if size == large:
        result = [
            "".join(map(
                lambda x: get_terrain(x, large_top, color)[0], names)),
            "".join(map(
                lambda x: get_terrain(x, large_bottom, color)[0], names))]
    else:
        result = ["".join(map(
            lambda x: get_terrain(x, size, color)[0], names))]
    return result


def print_terrain_row(names, size=large, color=True):
    print "\n".join(get_terrain_row(names, size, color))


def get_terrain_grid(rows, size=large, color=False):
    return map(lambda x: get_terrain_row(x, size, color), rows)


def print_terrain_grid(rows, size=large, color=True):
    print "\n".join(
        map(lambda x: "\n".join(get_terrain_row(x, size, color)), rows))
