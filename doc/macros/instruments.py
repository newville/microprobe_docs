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
#enddef
