def shutdown_server():
   """shutdown scan server:
     WARNING : only do this if you are sure!!
   """
   caput('13XRM:SCANDB:Shutdown', 1)
#enddef




def low_flux():
   caput('13IDA:m6.VAL', 0.10)
   caput('13IDA:m8.VAL', 0.20)
   caput('13IDA:m70.VAL', 0.03)
   set_i0amp_gain(2, 'nA/V')
   sleep(10)
   set_mono_tilt()
#enddef

def high_flux():
   caput('13IDA:m6.VAL', 0.80)
   caput('13IDA:m8.VAL', 0.25)
   caput('13IDA:m70.VAL', 0.08)
   set_i0amp_gain(10, 'nA/V')
   sleep(10)
   set_mono_tilt()
#enddef

def focus2():
  "focus beam "
  move_instrument('Small KB Forces', 'focus_2um', wait=True)
#enddef

def focus10():
  "partial de-focus beam"
  move_instrument('Small KB Forces', 'focus_10um', wait=True)
#enddef

def focus50():
  "de-focus beam"
  move_instrument('Small KB Forces', 'focus_50um', wait=True)
#enddef

def set_slitsize(val):
  "set SSA Horizontal beamsize in microns"
  caput('13IDA:m70.VAL', val/1000.0)
#enddef


## Edit Macro text here
#

def feedback_off():
    caput('13IDA:efast_pitch_pid.FBON', 0)
    caput('13IDA:efast_roll_pid.FBON', 0)
#enddef


def detector_distance(val, pvname='13IDE:m19.VAL', wait=True):
    """move detector distance to stage position value

    Parameters
    ----------
    val:      number, nominal stage position
    pvname:   string, name of detector distance PV ('13IDE:m19.VAL')
    wait:     True/False, whether to wait for move to complete (True)

    Examples
    --------
      detector_distance(30)

    """
    print 'Moving Detector %s= %.3f (wait=%s)' % (pvname, val, wait)
    return caput(pvname, val, wait=wait)

 #enddef
