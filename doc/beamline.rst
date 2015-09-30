..  _beamline-chapter:

=====================================================
General X-ray Microprobe Beamline Capabilities
=====================================================

The X-ray microprobe at GSECARS uses an undulator beamline to provides
fluxes in the range of :math:`10^{10}` to :math:`10^{12}` Hz in a a few
square microns, over an energy range of 2.4 to 27 keV.  This beam can be
used for X-ray Fluorescence maps, X-ray absorption spectroscopy, and X-ray
diffraction.  The description of the X-ray microprobe beamline here is not
meant to be an exhaustive explanation, but to give guidance on using the
beamline effectively.

Spot Size
==============

The typical X-ray spot size is :math:`1 \times 2` :math:`\rm{\mu}m` using
Kirkpatrick-Baez (KB) mirrors which separately focus in the horizontal and
vertical directions.  The vertical beam is much easier to achieve a fine
focus and no additional optics are needed.  For the horizontal direction,
the beamline mirrors that are used to deflect the beam away from the
in-board branch line are also used to focus the beam onto an aperture, at
roughly 42 m from the undulator source.  By closing this *secondary source
aperture*, the re-diverging beam can be focused with the final mirror of
the KB pair.  By adjusting this secondary aperture, one can trade final
spot size for intensity.  The beamline normally operates with a slit that
passes about 20% of the full flux into about 2 :math:`\rm{\mu}m`.

Since X-rays penetrate deeply into most materials, typical sampling
:math:`1/e` depths range from 5 to 250 :math:`\rm{\mu}m`, with 50
:math:`\rm{\mu}m` being a good rule of thumb.


Energy Range
==============

The energy range for the GSECARS beamline is 2.4 to 27 keV.  The
monochromator has very reliable energy reading, and XAFS scans are easy.
Changing energy between elements is very easy between about 4 and 22 keV
and can be done from pre-defined scripts that not only move the
monochromator angle, but also move undulator harmonics and mirror coatings,
and does an automated search for the beam in order to be able to keep the
beam position stable during measurements.

It is normally possible to move between any X-ray edges in the 4 to 22 keV
range without thinking about it much, and to rely on automated energy
switching in overnight macro sequences.  Working below 4 keV or above 22
keV is not hard, but sometimes requires special care.

low energies
-------------

At low energies, say S and Cl K edges and other edges below 3 keV, we'll
almsot certainly want to put the sample in a He environment -- a very large
zip-lock bag.  For most higher energy work this bag is kind of nuisance, so
we normally do not have this in place.  Setting it up doesn't take very
long, but it means that we can't easily "just try" S K edge XANES.

In addition, the monochromator angle for Si(111) changes quite a bit
between 2.4 and 4 keV. Moving from 2.4 to 4.0 keV is a larger angular
change than moving from 4.0 to 20 keV.  This also cause a relatively large
change in beam *roll* (left-right steering) unless the monochromator
crystals are very close to parallel.  The automated energy moving scripts
can usually find the beam, but this is trickier (and can fail) when going
to low energy.  In short, Matt or Tony should be around the first time you
move to low energy, to make sure the scripts to move back and forth from
low to high energy are working well.

It is certainly possible to move between S and higher energies (say, up to
15 keV) multiple times per day, but we do recommend limiting the number of
times you do this, and to not expect switching to always be simple.



high energies
--------------

At high energies, say above 22 keV, and certainly above 24 keV, the GSE
microprobe is starting to lose flux, partly due to mirror cut-offs.
Steering the beam is usually not a problem, but the intensities fall below
:math:`10^{11}` Hz.  In addition, the sensitivity of the Si fluorescence
detectors is diminishing, and the penetration depth of X-rays into
materials is going down.  All this is to say that we observe that our
sensitivity is much lower for edges about 22 keV than we normally expect
from our experiene below 20 keV.


Positional Stability
======================

The monochromator deflects the beam vertically, and is meant to be `fixed
offset`.  To do this, the gap between the first and second monochromator
must be moved, which has some small (micron-level) instabilities.  In
addition, the fine pitch of the second crystal can be adjusted which moves
the beam vertically.  The overall stability is very good -- typically a few
microns at the X-ray Beam Position Monitor (around 41 m from the source,
just in front of the Secondary Source Aperture).  We *can* measure this and
use a feedback loop to stabilize the vertical beam position by adjusting
the pitch on the second crystal.  We do not normally do this, though at low
energies (high angles) we do use a "very slow feedback" process to keep the
vertical beam position stable.

The monochromator can also steer the beam horizontally (*roll*) if the two
crystals are not parallel.  The effect is small, but the microprobe
beamline also uses two mirrors (at 3 mrad) just after the monochromator to
deflect the beam horizontally that amplifies any horizontal motion from the
monochromator.  Because we focus the beam in the horizontal to about 350
microns, and slit this beam down to around 70 microms to make a Seconday
Source at 42 m from the source (and 16 m from the monochromator), a small
roll in the monochromator can have a big effect on beam intensity and
positional stability.  We normally *do* use a feedback loop to adjust the
beam position at the X-ray Beam Position Monitor.

With the Position essentially fixed to a few microns at the Secondary
Source point, the position of the final focus beam is very good, even over
large energy moves.  Unless we bump something on the table, that is.



Sample Stage
===================

In the Microprobe station, the sample normally sits at 45 degrees to the
incident beam, and is held in place by a large Sample Stage.


Sample Microscope
==============================

The sample microscope sits normal to the sample (so, 135 degrees to the
beam), and is used to locate the spot to analyze.  That is, we typically
put in a phosphorescent material to find the X-ray beam, then use the focal
plane of the optical microscope to know where the beam will hit the sample
That gives pretty good, but not perfect, precision.  Because it relies on
finding the focal plane, because the sample sits 45 degrees to the incident
beam, and and because of the penetrating nature of X-rays, the positional
precision is much less certain in the horizontaly than vertically.

The microscope gives a pretty good optical image of the sample of around
400 x 550 microns, using a 10x objective and a high resolution (1928x1440)
color CCD camera.  We sometimes use a 5x objective to give a larger field
of view.  The lighting can be either through-the-lens reflected light or a
lamp to give transmitted light.


X-ray Fluorescence Detector
==============================

The fluorescence detector used is a Vortex ME-4 silicon drift detector,
using Xspress3 electronics from Quantum, Inc.  Each of the 4 detector
elements can count up to about 3 MHz.  We normally try to run these at 1
MHz or less to avoid saturation -- this can be corrected but becomes noisy
above 3 MHz.  At low count rates (say, below 100 kHz), the spectral
resolution is very good: as low as 135 eV at 5.9 keV, which is as good as
one can do with a silicon detector.  The energy calibration is very good,
and stays stable with count rate and over time.


For XRF mapping, we slew the Sample Stage in the beam and trigger the
detector to collect 4 full spectra per pixel.  We're able to collect full
spectra in as short as 2 ms, though we typically use per-pixel dwell times
of 10 to 50 ms.


X-ray Diffraction Camera(s)
==============================

To do X-ray diffraction
