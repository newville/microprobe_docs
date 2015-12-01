..  _commands-chapter:

=========================
Available Commands
=========================

Being able to script data collection by writing a ``macro`` or **script**
of commands to execute is an important part of the EpicsScan data
collection system.  All of the commands described here can either be
executed one at a time from the command line, or run in a script.



Moving the Sample Stage
=======================================

Several commands allow you to move the sample to a desired location<.

.. module:: samplestage
   :synopsis: commands for moving the sample


.. autofunction:: move_samplestage

.. autofunction:: move_fine

Getting Positions from OSCAR to the Sample Stage
======================================================

These commands help move coordinates saved with OSCAR (the off-line
microscope) to the Samplestage.


.. module:: uscope

.. autofunction:: uscope2sample

.. autofunction:: make_uscope_rotation


Moving the Monochromator Energy
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

.. autofunction:: mirror_stripe

.. autofunction:: bpm_foil


Custom Energy Commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Several custom commands wrap these, to give experiment-specific commands.
Since these can change for each experiment, please consult Matt or Tony
before using them!

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


Running Scans
=======================================

There are several commands for running scans from the command line or from
a script.

.. module:: scanning
   :synopsis: commands for scanning

.. autofunction:: pos_scan
.. autofunction:: pos_map

.. autofunction:: line_scan
.. autofunction:: grid_scan
.. autofunction:: redox_map
.. autofunction:: grid_xrd



Collecting X-ray Diffraction Images
=======================================

.. automodule:: xrd

.. autofunction:: save_xrd
.. autofunction:: save_xrd_pe
.. autofunction:: save_xrd_marccd
.. autofunction:: xrd_bgr


Controlling the X-ray beam intensity
===========================================

.. automodule:: intensity

.. autofunction:: set_mono_tilt
.. autofunction:: optimize_id

.. autofunction:: feedback_off
.. autofunction:: collect_offsets
.. autofunction:: set_SRSgain
.. autofunction:: set_i1amp_gain
.. autofunction:: set_i0amp_gain
.. autofunction:: autoset_gain
.. autofunction:: autoset_i0amp_gain
.. autofunction:: autoset_i1amp_gain
.. autofunction:: autoset_i2amp_gain


Moving Other Beamline Instruments
==============================================

.. module:: instruments
   :synopsis:  instruments

.. autofunction:: detector_distance
.. autofunction:: set_SSA_hsize
.. autofunction:: move_instrument



The Pre-Scan Command
=======================================

.. automodule:: pre_scan_command

.. autofunction:: pre_scan_command
