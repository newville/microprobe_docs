# from common import check_abort_pause
# from instruments import bpm_foil, dhmirror_stripe
# from intensity import set_mono_tilt, autoset_i0amp_gain

IDPREF = 'S13ID:USID'

def select_id_harmonic(energy):
    id_harmonic = 1
    if energy >  8500:
        id_harmonic = 3
    elif energy > 15200:
        id_harmonic = 5

    return id_harmonic

def undulator_offset(energy, harmonic=1):
    """undulator offset in energy given mono energy"""
    if harmonic == 1:
        id_energy = energy * 1.0010 - 41.0
    elif harmonic == 3:
        id_energy = energy * 0.9944 - 75.0
    elif harmonic == 3:
        id_energy = energy * 0.9944 - 150.0
    return 0.001*(id_energy - energy)


def move_energy(energy, id_offset=None, id_harmonic=None, wait=True):
    """
    move energy to desired value, optionally specifying
    how to move the undulator.

    Parameters:
        energy (float):  Energy in eV
        id_offset (float or None):  Undulator Offset. (Undulator - mono energy, in keV).
             if None (default) the value will be set to 1.2% of mono energy (and in keV)
        id_harmonic (int or None): Undulator harmonic to use.
             if None (default) the value will not be changed
        wait (True or False): whether to wait for move to finish (default True).

    Examples:
       move_energy(5000,  id_offset=0.050, id_harmonic=1)

    """
    if check_abort_pause():
        return
    if id_harmonic is None:
        id_harmonic = select_id_harmonic(energy)
    id_harmonic_pv = get_pv(f'{IDPREF}:HarmonicValueC.VAL')
    id_gaptaper_pv = get_pv(f'{IDPREF}:TaperGapSetC.VAL')
    caput('13IDE:En:id_harmonic', id_harmonic)
    if 'write' in id_harmonic_pv.access:
        id_harmonic_pv.put(id_harmonic)
    else:
        print("no write access for harmonic")
    sleep(0.25)

    if id_offset is None:
        id_offset = undulator_offset(energy, harmonic=id_harmonic)
    caput('13IDE:En:id_off.VAL', id_offset)
    sleep(0.050)
    id_energy = 0.001*energy + id_offset
    id_energy_pv = get_pv(f'{IDPREF}:ScanEnergyC.VAL')
    # start undulator moving, if allowed
    if 'write' in id_energy_pv.access:
        # print("Put ID Energy ", id_energy_pv, id_energy)
        cur_id_en = id_energy_pv.get()
        id_energy_pv.put(id_energy - 0.1*(id_energy - cur_id_en), wait=False)
        sleep(0.1)
        id_gaptaper_pv.put(0.050)
        sleep(0.1)
        id_energy_pv.put(id_energy, wait=False)
    else:
        print("no write access for energy")
        print(id_energy_pv)
    #endif
    caput('13IDE:En:y2_track', 1)
    caput('13IDE:En:id_track', 1)
    caput('13IDE:En:id_wait',  0)
    sleep(0.1)
    caput('13IDE:En:Energy.VAL', energy, wait=wait)
    print("Move Energy done")


def _use_xtal(mono_x=4, mono_h=25.1, th_off=17.548321,
              x2_pitch=-0.106, x2_roll=1.06,
              dspace=3.13477,mirror_pitch=None):
    print("use xtal ", mono_x, mono_h, th_off, x2_pitch, x2_roll, dspace, mirror_pitch)
    if check_abort_pause():
        return

    energy = caget('13IDE:En:Energy')
    caput('13XRM:roll_pid.FBON', 0)
    caput('13IDA:m32',       mono_x)
    caput('13IDE:En:height', mono_h)
    caput('13IDA:m65.OFF',   th_off)
    caput('13IDA:m67.VAL',   x2_pitch)
    caput('13IDA:m68.VAL',   x2_roll)
    caput('13IDE:En:dspace', dspace)
    caput('13IDA:m32',       mono_x, wait=True)
    caput('13IDA:m67.VAL',   x2_pitch, wait=True)
    caput('13IDA:m68.VAL',   x2_roll, wait=True)
    if mirror_pitch is not None:
        caput('13IDA:pm18.VAL',  mirror_pitch, wait=True)
    #endif
    sleep(0.1)
    caput('13IDE:En:Energy', energy-5.0, wait=True)
    caput('13IDE:En:Energy', energy)
#enddef

def use_si111(with_tilt=True):
    """
    switch to Si(111)

    Parameters:
        energy (float): energy to set mono to.

    Note:
       Use with Caution!  Consult Matt or Tony first!

    """
    vals = {'mono_x':    caget('13IDE:userTran7.E'),
            'mono_h':    caget('13IDE:userTran7.C'),
            'th_off':    caget('13IDE:userTran7.G'),
            'x2_pitch':  caget('13IDE:userTran7.I'),
            'x2_roll':   caget('13IDE:userTran7.K'),
            'dspace':    caget('13IDE:userTran7.A')}

    _use_xtal(**vals)
    _scandb.set_info('experiment_monoxtal', 'Si(111)')
    if with_tilt:
        set_i0amp_gain(10, 'nA/V')
        set_mono_tilt()
        autoset_i0amp_gain()
    #endif
#enddef

def use_si311(with_tilt=True):
    """
    switch to Si(311)

    Parameters:
        energy (float): energy to set mono to.

    Note:
       Use with Caution!  Consult Matt or Tony first!

    """
    vals = {'mono_x':    caget('13IDE:userTran7.F'),
            'mono_h':    caget('13IDE:userTran7.D'),
            'th_off':    caget('13IDE:userTran7.H'),
            'x2_pitch':   caget('13IDE:userTran7.J'),
            'x2_roll':    caget('13IDE:userTran7.L'),
            'dspace':     caget('13IDE:userTran7.B'),}

    _use_xtal(**vals)
    _scandb.set_info('experiment_monoxtal', 'Si(311)')
    if with_tilt:
        set_i0amp_gain(5, 'nA/V')
        set_mono_tilt()
        autoset_i0amp_gain()
    #endif
#enddef

def move_to_edge(element, edge='K', id_harmonic=None, id_offset=None,
                 stripe=None, foil=None, with_tilt=True, waittime=1.0): #
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
    if check_abort_pause(): return
    edge_energy = xray_edge(element, edge)[0]
    if edge_energy > 36000 and edge == 'K':
        edge_energy = xray_edge(element, 'L3')[0]
    #endif
    # pick a nice round energy above the nominal edge
    energy = 25.0*(int((edge_energy*1.01)/25.0 + 1))

    # guess id harmonic
    if id_harmonic is None:
       id_harmonic = select_id_harmonic(energy)

    # guess foil
    if foil is None:
        foil = 'Au'
        ## print("Guess a good foil energy ", energy)
        if energy < 15000:   foil = 'Ni'
        if energy <  9100:   foil = 'Cr'
        if energy <  6900:   foil = 'Ti'
        if energy <  5300:   foil = 'Ni'
        if energy <  3300:   foil = 'Cr'
        #######
    #endif
    bpm_foil(foil)

    # guess mirror stripe
    if stripe is None:
        stripe = 'Si'
        if energy >  9500:  stripe = 'rh'
        if energy > 21000:  stripe = 'pt'
    #endif

    caput('13XRM:pitch_pid.FBON', 0)
    caput('13XRM:roll_pid.FBON', 0)

    # first move mirrors without waiting
    dhmirror_stripe(stripe=stripe, wait=False)

    id_scan_energy_pv = PV(f'{IDPREF}:ScanEnergyC.VAL')
    id_curr_energy_pv = PV(f'{IDPREF}:EnergyM.VAL')
    id_curr_energy = id_curr_energy_pv.get()
    id_scan_energy = id_scan_energy_pv.get()
    if id_scan_energy_pv.write_access:
        id_scan_energy_pv.put(id_scan_energy + 0.001)
    else:
        print("cannot move undulator")
        print(id_scan_energy_pv)
    #endif

    # move the energy
    move_energy(energy, id_offset=id_offset, id_harmonic=id_harmonic)

    # make sure mirrors are finished moving
    # before setting mono tilt
    dhmirror_stripe(stripe=stripe, wait=True)

    t0 = time()
    wait_for_id = True
    print("waiting for ID")
    ixx = 1.0
    while wait_for_id:
        sleep(1.0)
        ixx = -ixx
        id_curr_energy = id_curr_energy_pv.get()
        id_scan_energy = id_scan_energy_pv.get()
        if id_scan_energy_pv.write_access:
            id_scan_energy_pv.put(id_scan_energy + ixx*0.002)
            wait_for_id = ((time() - t0) < 30.0 and
                           abs(id_curr_energy - id_scan_energy) > 0.050)
        else:
            wait_for_id = False
        #endif
    #endwhile

    sleep(waittime)
    if with_tilt:
        set_mono_tilt()
    #endif
#enddef


def setup_trans_xafs(element, edge='K'):
    "move below edge, auto-set I1 amplifier"
    edge_energy = xray_edge(element, edge)[0]
    if edge_energy > 36000 and edge == 'K':
        edge_energy = xray_edge(element, 'L3')[0]
    #endif
    # pick a nice round energy at least 70 eV above nominal edge
    en_above = 25.0*(int((edge_energy+70.0)/25.0 + 1))
    en_below = 25.0*(int((edge_energy-50.0)/25.0 ))

    move_energy(en_below)
    autoset_i1amp_gain()
    move_energy(en_above)
#enddef
