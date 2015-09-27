..  _macros-chapter:

=========================
Available Commands
=========================

Being able to script data collection by writing a ``macro`` or **script**
of commands to execute is an important part of the EpicsScan data
collection system.  All of the commands described here can either be
executed one at a time from the command line, or run in a script.


.. module:: macrocode

Running Scans
=======================================

There are several commands for running scans from the command line or from
a script.

.. module:: scanning
   :synopsis: commands for scanning

.. autofunction:: pos_scan
.. autofunction:: pos_map

.. autofunction:: pre_scan_command
.. autofunction:: xafs_grid
.. autofunction:: loop_map
.. autofunction:: line_scan
.. autofunction:: redox_map
.. autofunction:: xrd_map

Moving the Sample Stage
=======================================

Several commands allow you to move the sample to a desired location<.

.. module:: samplestage
   :synopsis: commands for moving the sample

.. autofunction:: move_fine

.. autofunction:: move_samplestage


Moving The Monochromator Energy
=======================================

There are a couple general-purpose commands for moving the monochromator energy
to a particular energy or edge, and several specialized commands to move to
a particular edge which may also set other settings (Ion Chamber gains,
mirror stripes) and also do an automated search-and-optimization of the
beam intensity.

.. module:: energy
   :synopsis: commands for moving energy

.. autofunction:: move_energy

.. autofunction:: move_to_edge



.. autofunction::  move_to_s
.. autofunction::  move_to_ti
.. autofunction::  move_to_v
.. autofunction::  move_to_cr
.. autofunction::  move_to_mn
.. autofunction::  move_to_eu
.. autofunction::  move_to_fe
.. autofunction::  move_to_ni
.. autofunction::  move_to_cu
.. autofunction::  move_to_zn
.. autofunction::  move_to_w
.. autofunction::  move_to_as
.. autofunction::  move_to_sr
.. autofunction::  move_to_zr
.. autofunction::  move_to_mo


.. autofunction::  move_to_map

.. autofunction::  move_to_xrd
