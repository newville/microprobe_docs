..  _commands-chapter:

=========================
Available Commands
=========================

Being able to script data collection by writing a ``macro`` or
**script** of commands to execute is an important part of the
EpicsScan data collection system.  EpicsScan provides a **macro
interpreter** which uses a subset of the Python language.  There are
some restrictions on what can be done in the this macro interpreter,
but it is plenty powerful enough for data collection scripts.  All of
the commands described here can either be executed one at a time from
the command line, or run in a script.



Core Functions
=======================================

These functions are built into the macro interpreter and alwayas
available.  Most of these will not be useful as high-level macros
themselves, but can be used with macros to control data collection.

.. module:: epicsscan.macros_init

Epics Channel Access Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These provide access to Epics Channel Access (CA) variables used in
the control system.

.. autofunction:: caget
.. autofunction:: caput
.. autofunction:: get_pv

access to the EpicsScan Postgresql Database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These functions provide access the data in the PostgresQL database
used by the data collection system:


.. autofunction:: get_dbinfo
.. autofunction:: set_dbinfo
.. autofunction:: scan_from_db
.. autofunction:: check_scan_abort
.. autofunction:: move_instrument
.. autofunction:: move_samplestage

.. attribute:: _scandb
               direct acces to the EpicsScan database.

core scanning commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These are the basic commands to request a data collection scan

.. autofunction:: do_scan
.. autofunction:: do_slewscan


Xray Data functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These functions (from `xraydb`) provide X-ray data that may be useful
in macros:

.. autofunction:: atomic_mass
.. autofunction:: atomic_name
.. autofunction:: atomic_number
.. autofunction:: atomic_symbol
.. autofunction:: chemparse
.. autofunction:: etok
.. autofunction:: ktoe
.. autofunction:: get_material
.. autofunction:: guess_edge
.. autofunction:: ionchamber_fluxes
.. autofunction:: material_mu
.. autofunction:: material_mu_components
.. autofunction:: mirror_reflectivity
.. autofunction:: mu_elam
.. autofunction:: xray_edge
.. autofunction:: xray_edges
.. autofunction:: xray_line
.. autofunction:: xray_lines


.. autofunction:: clock
.. autofunction:: sleep
.. autofunction:: as_ndarray
.. autofunction:: index_nearest
.. autofunction:: index_of


Restarting the Scan Server
=======================================

.. module:: escan_macros.common

Two commands are available for restarting the Scan Server process are
reloading all macro definition.


.. autofunction:: restart_server

.. function:: load_macros()
              re-read and re-load all macros

   Reloads all Macro definitions.   This is necessary if you change a macro.
   Note that closing and reopening the `Macro Window` will do this.



Moving the Monochromator Energy
=======================================

There are a couple general-purpose commands for moving the monochromator energy
to a particular energy or edge, and several specialized commands to move to
a particular edge which may also set other settings (Ion Chamber gains,
mirror stripes) and also do an automated search-and-optimization of the
beam intensity.

.. module:: escan_macros.energy

   :synopsis: commands  moving energy

.. autofunction:: move_energy

.. autofunction:: move_to_edge

.. autofunction:: dhmirror_stripe

.. autofunction:: bpm_foil


Custom Energy Commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Several custom commands wrap these, to give experiment-specific commands.
Since these can change for each experiment, please consult Matt or Tony
before using them!


Running Scans
=======================================

There are several commands for running scans from the command line or from
a script.

.. module:: escan_macros.scanning
   :synopsis: commands for scanning

.. autofunction:: pos_scan
.. autofunction:: pos_map

.. autofunction:: line_scan
.. autofunction:: grid_scan
.. autofunction:: redox_map
.. autofunction:: grid_xrd


Collecting X-ray Diffraction Images
=======================================

.. module:: escan_macros.xrd
   :synopsis: commands for XRD

.. autofunction:: save_xrd
.. autofunction:: xrd_bgr



Controlling the X-ray beam intensity
===========================================

.. module:: escan_macros.intensity
   :synopsis: commands for controlling incident X-ray intensity

.. autofunction:: set_mono_tilt
.. autofunction:: collect_offsets
.. autofunction:: set_SRSgain
.. autofunction:: set_i0amp_gain
.. autofunction:: set_i1amp_gain

..
 autofunction:: autoset_gain
 autofunction:: autoset_i0amp_gain
 autofunction:: autoset_i1amp_gain
 autofunction:: autoset_i2amp_gain


Moving Other Beamline Instruments
==============================================

.. module:: escan_macros.instruments
   :synopsis:  instruments

.. autofunction:: detector_distance


The Pre-Scan Command
=======================================

.. module:: escan_macros.pre_scan

.. autofunction:: pre_scan_command
