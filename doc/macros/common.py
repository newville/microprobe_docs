def shutdown_server():
   """shutdown scan server:
     WARNING : only do this if you are sure!!
   """
   caput('13XRM:SCANDB:Shutdown', 1)
#enddef


def feedback_off():
    caput('13IDA:efast_pitch_pid.FBON', 0)
    caput('13IDA:efast_roll_pid.FBON', 0)
#enddef

def optimize_id():
    mono_energy = caget('13IDE:En:Energy')
    id_harmonic = caget('13IDE:En:id_harmonic')
    offset = (0.01 * mono_energy + (id_harmonic-1)*2.0)*1.e-3
    offset = max(0.010, min(0.300, offset))

    idvals = 1.e-3 * mono_en + linspace(0, 2, 21)*offset
    print 1.e-3 * mono_en, offset, idvals
    best_id = ivals[10]
    best_i0  = 0.0
    for idval in idvals:
       caput('ID13us:ScanEnergy', idval)
       sleep(0.5)
       caget('13IDE:scaler1.S2', i0)
       if i0 > best_i0:
          best_i0 = i0
          best_id = idval
       #endif
    #endfor
    print 'best ID ', best_i0, best_id
#enddef


def collect_offsets(t=10):
    '''collect scaler offsets'''
    # close shutter
    caput('13IDA:CloseEShutter.PROC', 1)
    # set scaler to 1 shot mode, count time of 10 seconds
    count_time =  caget('13IDE:scaler1.TP')

    caput('13IDE:scaler1.CONT', 0)
    caput('13IDE:scaler1.TP',   t)
    caput('13IDA:CloseEShutter.PROC', 1, wait=True)
    time.sleep(3.0)
    caput('13IDE:scaler1.CNT', 1, wait=True)
    time.sleep(0.5)
    # read clock ticks, and counts for each channel
    clock_count = 1.0*caget('13IDE:scaler1.S1')
    for i, name in ((2, 'B'), (3, 'C'), (4, 'D'), (5, 'E')):
       desc = caget('13IDE:scaler1.NM%i' % i)
       if len(desc) > 0:
          counts = caget('13IDE:scaler1.S%i'  % i)
          scale = counts/(clock_count)
          expr   = "%s-(A*%.6g)" % (name, scale)
          caput('13IDE:scaler1_calc%i.CALC' % i, expr)
       #endif
    #endfor
    # reset count time, put in auto-count mode, open shutter
    caput('13IDE:scaler1.TP',   count_time)
    caput('13IDE:scaler1.CONT', 1)
    caput('13IDA:OpenEShutter.PROC', 1)
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
