def shutdown_server():
   """
   shutdown, restart scan server.
   WARNING : only do this if you are sure of what you're doing!
   Consult Matt and Tony before using
   """
   caput('13XRM:SCANDB:Shutdown', 1)
#enddef


def low_flux():
   """
   Set to 'low flux' conditions
   Note that details vary for each user, and you should
   consult Matt and Tony before using
   """
   caput('13IDA:m6.VAL', 0.10)
   caput('13IDA:m8.VAL', 0.20)
   caput('13IDA:m70.VAL', 0.03)
   set_i0amp_gain(2, 'nA/V')
   sleep(10)
   set_mono_tilt()
#enddef

def high_flux():
   """
   Set to 'high flux' conditions.
   Note that details vary for each user, and you should
   consult Matt and Tony before using
   """
   caput('13IDA:m6.VAL', 0.80)
   caput('13IDA:m8.VAL', 0.25)
   caput('13IDA:m70.VAL', 0.08)
   set_i0amp_gain(10, 'nA/V')
   sleep(10)
   set_mono_tilt()
#enddef

def focus2():
   """
   Focus beam to approximately 2 microns.
   Note that details vary for each user, and you should
   consult Matt and Tony before using
   """
   move_instrument('Small KB Forces', 'focus_2um', wait=True)
#enddef

def focus10():
   """
   Focus beam to approximately 10 microns.
   Note that details vary for each user, and you should
   consult Matt and Tony before using
   """
   move_instrument('Small KB Forces', 'focus_10um', wait=True)
#enddef

def focus50():
   """
   Focus beam to approximately 50 microns.
   Note that details vary for each user, and you should
   consult Matt and Tony before using
   """
   move_instrument('Small KB Forces', 'focus_50um', wait=True)
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


def feedback_off():
    caput('13IDA:efast_pitch_pid.FBON', 0)
    caput('13IDA:efast_roll_pid.FBON', 0)
#enddef


def detector_distance(val, pvname='13IDE:m19.VAL', wait=True):
    """
    Set Sample-detector distance

    Args:
        val (float):  Sample-detector distance in mm.
        pvname (string): Epics PV for sample-detector distance ['13IDE:m19.VAL']
        wait (True or False):  whether to wait for move to complete (True)

    Example:
        detector_distance(30)
    """
    print 'Moving Detector %s= %.3f (wait=%s)' % (pvname, val, wait)
    return caput(pvname, val, wait=wait)
#enddef
