~~~~
TODO
~~~~

As one might imagine, I have pages and pages of hand-written notes. I'll only
transfer them to this TODO file when I plan on working on noted features in
the "near" future (i.e., next up on the list).


Quick Tasks
===========

* Move the service code into a single module.

* Devise a means of loading games via configuration.

* Device a means of loading games via command line switches

* Run the example games as part of the Twisted plugin

* Update configuration so that there can be mutliple game configs in the
  config.ini and any one may be loaded by section name

* update HELP to include MAP command

* whereever there are print statements, replace with an object that writes to
  the terminal


Commands and Interpreter
========================

* Add save/restore game functionality.

  - add LOAD command

  - add SAVE command

* Add readline support (in particular, command history) for the interpreter.

* Add a Twisted ssh example

  - set the shell to the interactive game itself

  - make changes to allow for multiple users


Testing
=======

* Adjust the API so that it's testable

  - convert print statements to print methods that simply print the results of
    various actions, and then

  - use the "get" methods in tests (as opposed to the "print" methods

  - enable playing the example games programmatically (maybe scripting?)


Terrain
=======

* Work on defining terrain data and auto-populating a new world with tiles of
  different terrain types.

* The Cave terrain class was removed. Instead, an attirbute needs to be added
  to terrain objects to indicate the liklihood of a cave occurring on that
  tile.

* I've started thinking about the rules for fine-tuning the placement of tiles,
  and under what circumstances one tile can be next to another (in addition to
  valid transitions). This work needs to continue with the addition of
  supporting logic in the util.getRandomTileTransitionClass function.

* Exits need to be set up on terrain tiles.

* An ASCII road map can probably be extracted from the terrain grid with each
  tile providing exit data.

* Similarly, with ASCII representations of the terrain types, we could generate
  and ASCII physical map.

* Need to add unit tests for setExits on GeneratedMap and
  util.getSurroundingExits.


Scapes, Tiles and Worlds
========================

I've started to rename "scapes" to "tiles". However, the world object has a
scapes attribute... and to rename that to "tiles" wouldn't be accurate.

For instance:

* the ourdoor view of the world will have a definite number of tiles

* a certain number of these will be town or city tiles

* each town or city will be able to hold any number of buildings

* any building, a number of floors

* any room, a number of rooms

* similarly goes for caves - a single tile may have on or two caves, and those
  caves any number of cavern rooms and tunnels

So this makes me thing we need a "views", "layers", or "contexts" attribute for
the world. Each context would have it's own tile count, and depending upon
context, these would be terrain tiles, cityscape tiles, floor tiles, room
tiles, cave/dungeon tiles, etc.

Since memory usage could get quite large, it'd be a good idea to store each
context on disk until needed. For large maps (tile layouts for contexts), it
might be a really good idea to write portions to disk.

Hrm, actually, these contexts fit nicely with tree graphs...

This work should probably joined with the load/save work (the only difference
being the data, and explicit commands; the underlying plumbing will be the
same).


Directions
==========

Constants have been defined for directions now. Much of the code that was used
to get keys and values for direction dicts may no longer be necessary.
