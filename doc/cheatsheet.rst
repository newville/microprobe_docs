..  _cheatsheet-chapter:

Cheatsheet: Common Commands
======================================


This is a list of the most commonly used macro commands to use in the
Macro command window.  A full listing is given the the following chapter.


Running Scans
~~~~~~~~~~~~~~~~~~~~~~~~~

.. function::  pos_scan('my_sample', 'Scan1', number=3)

  move sample stage to position named from Sample Stage, and run named scan
  (XAFS or Slew Scan). Use 'number' to set multiple scans

.. function:: loop_map('my_sample', 'Scan1', motor='y', start=0, stop=0.1, step=0.001)

  Run repeated maps while moving a 3rd motor in between each map: move to a
  named position from Sample Stage and run the named scan. Then move a
  motor from a start and stop value at a given step increment.

.. function:: redox_map('my_sample', 'Scan1', energies=[8000, 8100])

  run a Redox map: move to a named position, and run the named scan at a
  series of energies.


Moving Monochromator Energy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the general purpose :func:`move_to_energy`  function:


.. function:: move_to_energy('Fe', 'K')

  Move to just above the Fe K edge


.. function:: move_to_energy('Pb', 'L3')

  Move to just above the Pb L3 edge


to move to just about any energy.  These commands may move several beamline
components, and will generally run the :func:`set_mono_tilt` function.  We
may also write custom scripts like

.. function:: move_to_fe()

  Move to just above the Fe K edge


.. function:: move_to_s()

  Move to just above the S K edge

.. function:: move_to_map()

  Move to an energy appropriate for mapping (depends on experiment)


.. function:: move_to_xrd()

  Move to an energy appropriate for XRD (depends on experiment)


Adjusting Intensity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. function:: set_mono_tilt()

  Re-find and stabilize beam intensity in ion chamber.


.. function:: detector_distance(50)

  Set distance for XRF detector (min=40)

Moving the Sample Stage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. function:: move_samplestage('MySpot')

   move samplestage to a named position.



Collecting XRD Images
~~~~~~~~~~~~~~~~~~~~~

.. function:: save_xrd('SampleX', t=10)

   collect a diffraction pattern for `t` seconds, save TIFF image to file



.. function:: xrd_bgr()

   take a background image for the XRD camera
