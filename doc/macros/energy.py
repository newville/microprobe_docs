"""
Commands for moving the monochromator energy and related tasks.
"""
from intensity import set_mono_tilt, autoset_i0amp_gain
from instruments import (move_instrument, smallkb_stripes,  mirrors_5mrad, mirrors_4mrad)

def move_energy(energy, id_offset=None, id_harmonic=None, wait=True):
    """
    move energy to desired value, optionally specifying
    how to move the undulator.

    Parameters:
        energy (float):  Energy in eV
        id_offset (float or None):  Undulator Offset. (Undulator - mono energy, in keV).
             if None (default) the value will not be changed
        id_harmonic (int or None): Undulator harmonic to use.
             if None (default) the value will not be changed
        wait (True or False): whether to wait for move to finish (default True).

    Examples:
       move_energy(5000,  id_offset=0.050, id_harmonic=1)

    """
    if id_harmonic is not None:
        caput('13IDE:En:id_harmonic.VAL', id_harmonic)
        caput('ID13us:HarmonicValue.VAL', id_harmonic)
    #endif

    if id_offset is not None:
        caput('13IDE:En:id_off.VAL', id_offset)
    #endif
    id_offset = caget('13IDE:En:id_off.VAL')

    sleep(0.10)

    id_energy = 0.001*energy + id_offset - 0.010
    caput('ID13us:ScanEnergy.VAL', id_energy)
    caput('13IDE:En:y2_track', 1)
    caput('13IDE:En:id_track', 1)
    caput('13IDE:En:id_wait',  0)
    sleep(0.50)
    caput('13IDE:En:Energy.VAL', energy, wait=wait)
    sleep(0.50)
#enddef


def use_si111(energy=7200):
    """
    switch to Si(111)

    Parameters:
        energy (float): energy to set mono to.

    Note:
       Use with Caution!  Consult Matt or Tony first!

    """
    caput('13IDA:m32',        1.7)
    caput('13IDA:m65.OFF',   17.52533)
    caput('13IDA:m67.VAL',    -0.132)
    caput('13IDA:m68.VAL',     0.980)
    caput('13IDE:En:dspace', 3.13477)
    caput('13IDA:m66.OFF',    13.4306)
    caput('13IDA:m32',         1.7, wait=True)
    sleep(3.0)
    caput('13IDE:En:Energy', energy+0.1)
    caput('13IDE:En:Energy', energy)
    # set_mono_tilt()
#enddef


def use_si311(energy=7200):
    """
    switch to Si(211)

    Parameters:
        energy (float): energy to set mono to.

    Note:
       Use with Caution!  Consult Matt or Tony first!

    """
    caput('13IDA:m32',        -1.85)
    caput('13IDA:m65.OFF',   17.62234)
    caput('13IDA:m67.VAL',     0.146)
    caput('13IDA:m68.VAL',     0.780)
    caput('13IDE:En:dspace', 1.63716)
    caput('13IDA:m66.OFF',    13.25)
    caput('13IDA:m32',        -1.85, wait=True)
    sleep(3.0)
    caput('13IDE:En:Energy', energy+0.1)
    caput('13IDE:En:Energy', energy)
    # set_mono_tilt()
#enddef


def bpm_foil(foilname):
    """
    select and move to BPM Foil by name

    Parameters:
        name (string): name of foil. One of
               'open', 'Ti', 'Cr', 'Ni', 'Al', 'Au'

    Note:
       not case-sensitive.

    Example:
       bpm_foil('Ni')

    """
    foilname = foilname.title()
    if foilname not in ('Open', 'Ti', 'Cr', 'Ni', 'Al', 'Au'):
       print("Unknown Foil Name '%s'"  % foilname)
       return
    #endif
    move_instrument('BPM Foil', foilname)
#enddef


def mirror_stripe(name='silicon', wait=True):
    """
    move beamline mirrors to a particular stripe by name

    Parameters:
        name (string): name of stripe. One of
            'silicon', 'rhodium', 'platinum' ['silicon']
        wait (True or False): whether to wait for move
            to complete before returning [True]

    Note:
        the first letter of the stripe ('s', 'r', 'p') is
        sufficient.

    Example:
        mirror_stripe('rh')

    """
    mirror_vals = {'s': (-0.2, -0.4, 0.),
                   'r': (10.4, 10.2, 10.6),
                   'p': (-8.0, -8.2, -7.8)}

    name = name[0].lower()
    vals = mirror_vals[name]
    caput('13IDA:m10.VAL', vals[0], wait=False)
    caput('13IDA:m11.VAL', vals[1], wait=False)
    caput('13IDA:m12.VAL', vals[2], wait=False)
    if wait:
        caput('13IDA:m10.VAL', vals[0], wait=True)
        caput('13IDA:m11.VAL', vals[1], wait=True)
        caput('13IDA:m12.VAL', vals[2], wait=True)
    #endif
#enddef

def move_to_edge(element, edge='K', id_harmonic=None, id_offset=None,
                 stripe=None, foil=None, with_tilt=True):
    """move energy to just above the edge of an element

    Parameters:
        element (str):  atomic symbol for element
        edge (str):  edge name ('K', 'L3', 'L2', 'L1', 'M')
        id_offset (float or None):  Undulator Offset, the
             undulator - mono energy in keV.
             if None (default) the value will not be changed
        id_harmonic (int or None): Undulator harmonic to use.
             if None (default) the value will not be changed
        stripe (str or None): name of mirror coating for beamline mirrors
             one of 'Si', 'Rh', 'Pt'
             if None (default) the stripe will be chosen based on energy.
        foil (str or None): name of foil to use in X-ray Beam Position Monitor.
             one of 'Au', 'Ni', 'Cr', 'Ti', or 'Al'
             if None (default) the foil will be chosen based on energy.
        with_tilt (bool): whether to adjust mono tilt [True]

    Examples:
       move_to_edge('V', 'K')

       move_to_edge('W', 'L3', stripe='Rh', with_tilt=False)

    """

    edge_energy = xray_edge(element, edge)[0]
    if edge_energy > 36000 and edge == 'K':
        edge_energy = xray_edge(element, 'L3')[0]
    #endif
    # pick a nice round energy at least 70 eV above nominal edge
    energy = 25.0*(int((edge_energy+70.0)/25.0 + 1))

    # guess id harmonic
    if id_harmonic is None:
       id_harmonic = 5
       if energy < 21000: id_harmonic = 3
       if energy <  9900: id_harmonic = 1
    #endif

    # guess id offset
    # as  mono_energy + 1%
    if id_offset is None:
       id_offset = (0.01 * energy + (id_harmonic-1)*2.0)*1.e-3
       id_offset = max(0.010, min(0.200, id_offset))
    #endif

    # guess foil
    if foil is None:
        foil = 'Au'
        if energy < 15000:  foil = 'Ni'
        if energy <  9100:  foil = 'Cr'
        if energy <  6400:  foil = 'Ti'
        if energy <  5300:  foil = 'Au'
        if energy <  3300:  foil = 'Cr'
    #endif
    # print(" --  Move to Edge Foil=", foil, energy)
    bpm_foil(foil)

    # guess mirror stripe
    if stripe is None:
        stripe = 'Si'
        if energy >  8800:  stripe = 'rh'
        if energy > 22000:  stripe = 'pt'
    #endif

    # first move mirrors without waiting
    mirror_stripe(name=stripe, wait=False)

    # actually move the energy
    move_energy(energy, id_offset=id_offset, id_harmonic=id_harmonic)

    # make sure mirrors are finished moving
    # before setting mono tilt
    mirror_stripe(name=stripe, wait=True)

    if with_tilt:
        sleep(1.0)
        set_mono_tilt()
    #endif
#enddef


def move_to_18kev():
     "move to 18.0 keV "
     move_to_edge('Zr', id_offset=0.210, id_harmonic=3, with_tilt=False)
     set_i0amp_gain(2, 'nA/V')
     move_energy(18000.0, id_offset=0.210)
     set_mono_tilt()
#enddef
#
# def move_to_14kev():
#     "move to 14.0 keV "
#     move_to_edge('Br', id_harmonic=3, with_tilt=False)
#     set_i0amp_gain(5, 'nA/V')
#     move_energy(14000.0)
#     set_mono_tilt()
# #enddef
#
# def move_to_12kev():
#     "move to 12.0 keV "
#     move_to_edge('As', id_harmonic=3, with_tilt=False)
#     set_i0amp_gain(5, 'nA/V')
#     move_energy(12000.0)
#     set_mono_tilt()
# #enddef
#
#
#
# def move_to_map():
#     "move to 12.5 keV  "
#     move_to_edge('Se', 'K',  with_tilt=False)
#     set_i0amp_gain(2, 'nA/V')
#     move_energy(12500.0, id_offset=0.14)
#     set_mono_tilt()
# #enddef
#
# def move_to_u():
#     "move to U L3 Edge"
#     set_i0amp_gain(2,  'nA/V')
#     move_to_edge('U', 'L3', id_offset=0.175, id_harmonic=3)
# #enddef
#
# def move_to_pb():
#     "move to Pb L3 Edge"
#     move_to_edge('Pb', 'L3', id_offset=0.145, foil='Ni')
#     autoset_i0amp_gain()
# #enddef
#
# def move_to_ti():
#     "move to Ti K Edge"
#     set_i0amp_gain(10, 'nA/V')
#     move_to_edge('Ti', id_offset=0.050, foil='Au')
#     set_mono_tilt()
# #enddef
#
# def move_to_v():
#     "move to V K Edge"
#     move_to_edge('V', id_offset=0.040)
# #enddef
#
# def move_to_cr():
#     "move to Cr K Edge"
#     set_i0amp_gain(10, 'nA/V')
#     move_to_edge('Cr', id_offset=0.070, foil='Ti')
# #enddef
#
# def move_to_mn():
#     "move to Mn K Edge"
#     set_i0amp_gain(10, 'nA/V')
#     move_to_edge('Mn', id_offset=0.062)
# #enddef
#
# def move_to_hg():
#     "move to Hg L3 Edge"
#     set_i0amp_gain(2, 'nA/V')
#     move_to_edge('Hg','L3', id_offset=0.128)
# #enddef
#
# def move_to_eu():
#     "move to Eu L3 Edge"
#     set_i0amp_gain(10, 'nA/V')
#     move_to_edge('Eu', edge='L3')
# #enddef
#


#
# def move_to_cl():
#     "move to Cl K Edge"
#     set_i0amp_gain(5,  'nA/V')
#     move_to_edge('Cl', id_offset=0.030)
# #enddef
# def move_to_br():
#     "move to Br K Edge"
#     set_i0amp_gain(5,  'nA/V')
#     move_to_edge('Br', id_offset=0.130)
# #enddef
#
#
# def move_to_s():
#     "move to S K Edge"
#     caput('13IDA:DAC1_7.VAL', 6.5)
#     caput('13IDA:DAC1_8.VAL', 5.0)
#     set_i0amp_gain(5, 'nA/V')
#
#     move_to_edge('S', id_offset=0.030, foil='Cr', with_tilt=False)
#     set_mono_tilt(enable_fb_roll=True, enable_fb_pitch=True)
# #enddef
#
#
# def move_to_cu():
#     "move to Cu K Edge"
#     set_i0amp_gain(5, 'nA/V')
#     move_to_edge('Cu', id_offset=0.090, id_harmonic=1)
# #enddef
#
# def move_to_ni():
#     "move to Ni K Edge"
#     set_i0amp_gain(10, 'nA/V')
#     move_to_edge('Ni', id_offset=0.080, id_harmonic=3)
# #enddef
#
# def move_to_zn():
#     "move to Zn K Edge"
#     set_i0amp_gain(20, 'nA/V')
#     move_to_edge('Zn', id_offset=0.098, id_harmonic=1)
# #enddef
#
#
#
# def move_to_sr():
#     "move to Sr K Edge"
#     set_i0amp_gain(5, 'nA/V')
#     move_to_edge('Sr', id_offset=0.130, id_harmonic=3)
# #enddef
#
# def move_to_zr():
#     "move to Zr K Edge"
#     set_i0amp_gain(2, 'nA/V')
#     move_to_edge('Zr', id_offset=0.140, id_harmonic=3)
# #enddef
#
# def move_to_mo():
#     "move to Mo K Edge"
#     set_i0amp_gain(2, 'nA/V')
#     move_to_edge('Mo', id_offset=0.150, id_harmonic=3)
# #enddef
#
#
# def move_to_se():
#     "move to Se K edge"
#     set_i0amp_gain(2, 'nA/V')
#     set_i1amp_gain(2, 'nA/V')
#     move_to_edge('Se', id_offset=0.178)
# #enddef
#
# def move_to_w():
#     "move to W L3 Edge"
#     set_i0amp_gain(20,  'nA/V')
#     caput('13IDA:DAC1_7.VAL', 3.46)
#     caput('13IDA:DAC1_8.VAL', 6.77)
#     move_to_edge('W', 'L3', id_offset=0.106)
# #enddef
#
#
#
#
# def move_to_as():
#     "move to As K edge"
#     set_i0amp_gain(5, 'nA/V')
#     move_to_edge('As', id_offset=0.117)
# #enddef
#
# def move_to_cs():
#     "move to Cs L3 edge"
#     set_i0amp_gain(20, 'nA/V')
#     move_to_edge('Cs', 'L3', with_tilt=False)
#     set_mono_tilt(enable_fb_roll=False)
# #enddef
#
# def move_to_re():
#     "move to Re L3 edge"
#     set_i0amp_gain(5, 'nA/V')
#     move_to_edge('Re', 'L3')
# #enddef#
#
# def move_to_cu():
#      "move to Cu K Edge"
#      set_i0amp_gain(5, 'nA/V')
#      move_to_edge('Cu', id_offset=0.090, id_harmonic=1)
# #enddef
#
# def move_to_ni():
#      "move to Ni K Edge"
#      set_i0amp_gain(5, 'nA/V')
#      move_to_edge('Ni','K')
# #enddef
#
# def move_to_zn():
#     "move to Zn K Edge"
#     set_i0amp_gain(5, 'nA/V')
#     move_to_edge('Zn', id_offset=0.098, id_harmonic=1)
# #enddef
#
#

def move_to_fe():
    "move to Fe K Edge"
    set_i0amp_gain(10,  'nA/V')
    move_to_edge('Fe', id_offset=0.070)
#enddef


def move_to_s():
    "move to S K Edge"
    set_i0amp_gain(5, 'nA/V')
    mirrors_5mrad()
    move_to_edge('Ca', id_harmonic=1)
    move_to_edge('S', id_harmonic=1)
#enddef

def move_to_xrd():
    "move to 18 keV"
    set_i0amp_gain(2, 'nA/V')
    mirrors_4mrad()
    move_to_edge('Zr', id_harmonic=3, with_tilt=False)
    move_energy(18000)
    set_mono_tilt()
#enddef

def move_to_pb():
    "move to 10 keV"
    set_i0amp_gain(2, 'nA/V')
    mirrors_4mrad()
    move_to_edge('Pb', edge='L3', id_harmonic=3)
#enddef

def move_to_map():
    "move to generic mapping energy"
    move_to_18keV()
#enddef
#
