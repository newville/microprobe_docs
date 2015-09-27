# run('common_macros.lar')
# run('scan_macros.lar')
# run('samplestage.lar')

import time

##
## Macros for moving instruments
##

def move_instrument(inst_name, position_name, wait=False,
                    prefix='13XRM:Inst:', timeout=60.0):
    """move an Epics Instrument to a named position

    Parameters
    ----------
    inst_name:      string, name of Epics Instrument
    position_name:  string, name of position for the Instrument
    wait:           True/False, whether to wait for move to complete (False)
    prefix:         string PV prefix used by Epics Instrument ('13XRM:Inst:')
    timeout:        time in seconds to give up waiting

    Examples
    --------
      move_instrument('Double H Mirror Stripes', 'platinum', wait=True)

    Notes
    ------
    This requires a working Epics Instrument program to be running.

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

def check_scan_abort():
    "returns whether Abort has been requested"
    return get_dbinfo('request_abort', as_bool=True)
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


def feedback_off():
    caput('13IDA:efast_pitch_pid.FBON', 0)
    caput('13IDA:efast_roll_pid.FBON', 0)
#enddef
