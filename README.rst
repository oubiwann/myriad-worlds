
~~~~~~~~~~~~~
Myriad Worlds
~~~~~~~~~~~~~

About
=====

.. image:: myriad-worlds/raw/master/resources/images/myriad-worlds-192.jpg
    :alt: Myriad Worlds Logo
    :align: right

This project is an experiment in generating worlds, stories, and interactive
fiction games. It attempts to do all this with a heritage of the classic
text-based adventure games -- as well as continuously drawing on them for
future inspiration. More than a game engine to power text adventures, this
project aims to be a framework for generating worlds -- and stories within
those worlds -- that are compelling, dynamic, and unpredictable.

History
-------

This code is based on the `adventure engine`_ that `Paul McGuire`_, the author
of PyParsing_, wrote and then summarized for a `PyCon 2006 talk`_. The first
revision in the myriad-worlds repository is his work, 100%.


Vision
------

Each subsequent revision since then has aimed to expand Paul's original work
into something that could support an experiment in authoring interactive
fiction adventure games. The initial thrust of this experimentation was:

* object- or connection-based storyline generation (as opposed to room-based)
  but this quickly expanded into exploring the following:

  * ASCII maps generated from textual descriptions

  * procedurally generated floor plans, city plans, landscapes, etc.

  * how to abstract a world and the narration of its contents in a way amenable
    to generating new stories from rearranged content

Ultimately, the intent of this project is to be able to create interesting
games that are infinitely replayable, due to the variation that is possible.


Usage
=====


Running the Examples
--------------------

Currently, you can run any of the examples that have a game module by pointing
your Python interpreter at the ``game.py`` file::

  $ python ./examples/house-adventure-2/game.py


Running a Server
----------------

TBD


Project Management
==================

Bugs are tracked using Launchpad:

* https://bugs.launchpad.net/myriad-worlds

Development plans, if any exist, are managed using Launchpad blueprints:

* https://blueprints.launchpad.net/myriad-worlds

Development tasks are managed using a correlation between blueprints and the
issue tracker. Each blueprint has a list of associated "bugs."


.. Document Links
   ==============

.. _adventure engine: http://www.ptmcg.com/geo/python/confs/adventureEngine.py

.. _Paul McGuire: http://www.oreillynet.com/pub/au/2557

.. _PyParsing: http://pyparsing.wikispaces.com/

.. _PyCon 2006 talk: http://www.ptmcg.com/geo/python/confs/pyCon2006_pres2.html
