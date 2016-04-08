### from epics import caput, caget

def detector_distance(val, pvname='13IDE:m19.VAL', wait=True):
    """
    Set Sample-detector distance in mm.

    Args:
        val (float):  Sample-detector distance in mm.
        pvname (string): Epics PV for sample-detector distance ['13IDE:m19.VAL']
        wait (True or False):  whether to wait for move to complete [True]

    Example:
        detector_distance(30)
    """
    print 'Moving Detector %s= %.3f (wait=%s)' % (pvname, val, wait)
    return caput(pvname, val, wait=wait)
#enddef


def dxd(val, pvname='13IDE:m19.VAL', wait=True):
    """
    m
    """
    print 'This is DXD'
    #     return caput(pvname, val, wait=wait)
#enddef



def set_SSA_hsize(val):
   """
   set SSA Horizontal beamsize, in microns.

   Args:
       val (float): SSA slit size in microns

   Example:
      set_SSA_hsze(50)
   """
   caput('13IDA:m70.VAL', val/1000.0)
#enddef


def move_instrument(inst_name, position_name, wait=False,
                    prefix='13XRM:Inst:', timeout=60.0):
    """move an Epics Instrument to a named position

    Parameters:
        inst_name (string): name of Epics Instrument
        position_name (string):  name of position for the Instrument
        wait (True or False): whether to wait for move to complete [False]
        prefix (string): PV prefix used by Epics Instrument ['13XRM:Inst:']
        timeout (float): time in seconds to give up waiting [60]

    Examples:
        move_instrument('Double H Mirror Stripes', 'platinum', wait=True)

    Note:
        requires a working Epics Instrument program to be running.

    """
    caput(prefix + 'InstName', inst_name)
    caput(prefix + 'PosName', position_name)
    sleep(0.25)
    if (caget(prefix + 'InstOK') == 1 and
        caget(prefix + 'PosOK') == 1):
        caput(prefix + 'Move', 1)
        if wait:
            moving, t0 = 1, clock()
            while moving:
                sleep(0.25)
                moving = ((1 == caget(prefix + 'Move')) or
                          (clock()-t0 > timeout))
            #endwhile
        #endif
    #endif
    sleep(1)
#enddef

def smallkb_stripes(stripe_name):
    """move small KB mirrors to a metal stripe by name

    Parameters:
        stripe_name (string): name of stripe, one of 'S', 'R', or 'P'

    Examples:
        smallkb_stripes('silicon')

    Note:
        requires a working Epics Instrument program to be running.

    """
    stripes = {'s':'silicon stripes',
               'r': 'rhodium stripes',
               'p': 'platinum stripes'}
    name = stripes.get(stripe_name.lower()[0], None)
    if name is None:
        print 'Unknown stripe name ', stripe_name
    else:
        move_instrument('Small KB Mirror Stripes', name, wait=True)
    #endif
#enddef

def mirrors_5mrad(stripe='si'):
    move_instrument('Small KB Forces', '5mrad', wait=True)
    smallkb_stripes(stripe)
    move_instrument('Sample Microscope', '5mrad', wait=True)
#enddef

def mirrors_4mrad(stripe='rh'):
    move_instrument('Small KB Forces', '4mrad', wait=True)
    smallkb_stripes(stripe)
    move_instrument('Sample Microscope', '4mrad', wait=True)
#enddef

def focus_2um():
    """move small KB mirrors to 2 microns
    """
    move_instrument('Small KB Forces', 'focus_2um', wait=True)
#enddef

def focus_50um():
    """move small KB mirrors to 50 microns
    """
    move_instrument('Small KB Forces', 'focus_50um', wait=True)
#enddef
