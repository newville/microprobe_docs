"""
Commands for setting intensities and Ion Chamber gains
"""
import time
def feedback_off():
    """
    Turn intensity feedback off
    """
    caput('13IDA:efast_pitch_pid.FBON', 0)
    caput('13XRM:edb:use_fb', 0)
    caput('13IDA:efast_roll_pid.FBON', 0)
#enddef

def feedback_on(roll=True, pitch=True):
    """
    Turn intensity feedback on or off

    roll = True / False for roll feedback
    pitch = True / False for pitch feedback
    """
    caput('13IDA:efast_pitch_pid.FBON', 0)
    caput('13XRM:edb:use_fb', 0)
    caput('13IDA:efast_roll_pid.FBON', 0)
    if pitch: caput('13XRM:edb:use_fb', 1)
    if roll:  caput('13IDA:efast_roll_pid.FBON', 0)

#enddef

def optimize_id():
    """
    Optimize undulator by scanning ID energy and
    finding highest I0 intensity

    Example:
        optimize_id()
    """
    caput('13IDE:En:id_track', 0)
    und_energy  = caget('ID13us:ScanEnergy')
    mono_energy = caget('13IDE:En:Energy')
    energies = linspace(-75, 75, 31) + mono_energy
    caput('13IDE:En:Energy', energies[0])
    sleep(2.0)
    best_en  = mono_energy
    best_i0  = -10.0
    i0vals = []
    for en in energies:
       caput('13IDE:En:Energy', en, wait=True)
       sleep(1.00)
       i0val = caget('13IDE:scaler1.S2')
       i0vals.append(i0val)
       if i0val > best_i0:
         best_i0 = i0val
         best_en = en
       #endif
    #endfor
    caput('13IDE:En:id_track', 1)
    offset = und_energy - best_en*0.001
    print 'best ID offset = %.3f keV ' % offset
    caput('13IDE:En:id_off', offset)
    caput('13IDE:En:Energy', best_en)
#enddef



def collect_offsets(t=10):
    """
    Collect dark-current offsets for Ion chameber scalers

    Parameters:
        t (float):  time in seconds to count dark current for (default 10)

    Examples:
        collect_offsets()
    """
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

def set_SRSgain(sens, unit, prefix='13IDE:A1', offset=100):
    """
    set pre-amplifier sensitivity, units, and offset

    Parameters:
        sens (int):  Number for sensitivity.
            One of (1, 2, 5, 10, 20, 50, 100, 200, 500).
        units (string): Unit sring.
            One of  ('pA/V', 'nA/V', 'uA/V', 'mA/V').
        prefix (string): PV prefix for SRS570 amplifier [default '13IIDE:A1']
        offset (float):  Input current offset for amplifier [default 100]

    Example:
       set_SRSgain(100, 'nA/V', prefix='13IDE:A2', offset=105)

    """
    steps = [1, 2, 5, 10, 20, 50, 100, 200, 500]
    units = ['pa/v', 'na/v','ua/v', 'ma/v']

    sens_val = steps.index(sens)
    unit_val = units.index(unit.lower())

    caput("%ssens_unit.VAL" % prefix, unit_val)
    caput("%ssens_num.VAL"  % prefix, sens_val)
    if sens_val > 2:
        sens_val -= 3
    else:
        sens_val += 6
        unit_val -= 1
    #endif
    caput("%soffset_unit.VAL" % prefix, unit_val)
    caput("%soffset_num.VAL"  % prefix, sens_val)
    caput("%soff_u_put.VAL"   % prefix, offset)
#enddef

def set_i1amp_gain(sens, unit, offset=100):
    """
    set I1 pre-amplifier sensitivity, units, and offset

    Parameters:
        sens (int):  Number for sensitivity.
            One of (1, 2, 5, 10, 20, 50, 100, 200, 500).
        units (string): Unit sring.
            One of  ('pA/V', 'nA/V', 'uA/V', 'mA/V').
        prefix (string): PV prefix for SRS570 amplifier [default '13IIDE:A1']
        offset (float):  Input current offset for amplifier [default 100]

    Examples:
        set_i1amp_gain(100, 'nA/V')
    """
    set_SRSgain(sens, unit, prefix='13IDE:A2', offset=offset)
#enddef

def set_i0amp_gain(sens, unit, offset=100):
    """
    set I0 pre-amplifier sensitivity, units, and offset

    Parameters:
        sens (int):  Number for sensitivity.
            One of (1, 2, 5, 10, 20, 50, 100, 200, 500).
        units (string): Unit sring.
            One of  ('pA/V', 'nA/V', 'uA/V', 'mA/V').
        prefix (string): PV prefix for SRS570 amplifier [default '13IIDE:A1']
        offset (float):  Input current offset for amplifier [default 100]

    Examples:
        set_i0amp_gain(100, 'nA/V')

    """
    set_SRSgain(sens, unit, prefix='13IDE:A1', offset=offset)
#enddef


def autoset_gain(prefix='13IDE:A1', scaler='13IDE:scaler1.S2', offset=100, count=0):
    """
    automatically set i0 gain to be in range

    Parameters:
       prefix (string): PV name for SRS570.
       scaler (string): PV name for scaler reading to use for reading intensity.
       offset (float):  Scaler offset value to use (default 100).
       count (int):     Recursion count to avoid infinite loop.

    Returns:
       success (True or False): whether setting the gain succeeded.
    """

    # limit number of attempts
    if count > 4:
        return False
    #endif

    ## make sure scaler is in autocount mode and that time is 1 sec
    sprefix  = scaler.split('.')[0]
    caput('%s.CONT' % sprefix, 0)
    caput('%s.TP1'  % sprefix, 1.0)
    caput('%s.TP'   % sprefix, 1.0)
    caput('%s.CNT'  % sprefix, 1, wait=True)
    unit = caget("%ssens_unit.VAL" % prefix)
    sens = caget("%ssens_num.VAL"  % prefix)
    sleep(0.01)
    i0 = caget(scaler)
    if i0 > 400000:
       sens = sens + 1
       if sens > 8:
           sens = 0
           unit = unit + 1
       #endif
    elif i0 < 80000:
       sens = sens - 1
       if sens < 0:
          sens = 8
          unit = unit - 1
       #endif
    else:
       return True
    #endif
    ## check that we haven't gone out of range
    if unit < 0 or unit > 3:
        print(" Unit out of range ", unit)
        return False
    #endif
    caput("%ssens_unit.VAL" % prefix, unit)
    caput("%ssens_num.VAL"  % prefix, sens)

    ## set offsets
    if sens > 2:
        off_sens = sens - 3
        off_unit = unit
    else:
        off_sens = sens + 6
        off_unit = unit - 1
    #endif
    if off_unit < 0:
        return False
    #endif
    caput("%soffset_unit.VAL" % prefix, off_unit)
    caput("%soffset_num.VAL"  % prefix, off_sens)
    caput("%soff_u_put.VAL"   % prefix, offset)
    caput("%sinit.PROC"       % prefix, 1)

    caput('%s.CNT'  % sprefix, 1, wait=True)
    sleep(0.010)
    i0 = caget(scaler)
    if (i0 < 80000) or (i0 > 400000):
       ok = autoset_gain(prefix=prefix, scaler=scaler, offset=offset, count=count+1)
       if not ok:
           return False
       #endif
    #endif
    caput('%s.CONT' % sprefix, 1)
    caput('%s.CNT'  % sprefix, 1)
    return True
#enddef

def autoset_i0amp_gain():
    autoset_gain(prefix='13IDE:A1', scaler='13IDE:scaler1.S2', offset=100)
    caput('13IDE:scaler1.CONT', 1)
    caput('13IDE:scaler1.CNT', 1)
#enddef

def autoset_i1amp_gain():
    autoset_gain(prefix='13IDE:A2', scaler='13IDE:scaler1.S3', offset=100)
    caput('13IDE:scaler1.CONT', 1)
    caput('13IDE:scaler1.CNT', 1)
#enddef

def autoset_i2amp_gain():
    autoset_gain(prefix='13IDE:A3', scaler='13IDE:scaler1.S4', offset=-100)
    caput('13IDE:scaler1.CONT', 1)
    caput('13IDE:scaler1.CNT', 1)
#enddef

def find_max_intensity(readpv, drivepv, vals, minval=0.1):
    """
    find a max in an intensity while sweeping through an
    array of drive values,  around a current position, and
    move to the position with max intensity.

    Parameters:
        readpv (string):   PV for reading intensity
        drivepv (string):  PV for driving positions
        vals (array of floats):  array of **RELATIVE** positions (from current value)
        minval (float):   minimum acceptable intensity [defualt = 0.1]

    Note:
       if the best intensity is below minval, the position is
       moved back to the original position.

    """
    _orig = _best = caget(drivepv)
    i0max = caget(readpv)
    for val in _orig+vals:
        caput(drivepv, val)
        sleep(0.100)
        i0 = caget(readpv)
        if i0 > i0max:
            i0max, _best = i0, val
        #endif
        if get_dbinfo('request_abort', as_bool=True): return
    #endfor
    if i0max < minval: _best = _orig
    caput(drivepv, _best)
    sleep(0.25)
    return i0max, _best
#enddef

def set_mono_tilt(enable_fb_roll=True, enable_fb_pitch=None):
    """
    Adjust IDE monochromator 2nd crystal tilt and roll to maximize intensity.

    Parameters:
        enable_fb_roll (True or False): enable roll feedback after
               best position is found. [True]
        enable_fb_pitch (True or False or None): enable pitch feedback after
               best position is found. [None]

    Note:
        This works by
            1. adjusting pitch to maximize intensity at BPM
            2. adjusting roll to maximize intensity at I0 Ion Chamber
            3. adjusting pitch to maximize intensity at I0 Ion Chamber

    """
    print 'Set Mono Tilt 23-Mar-2016'
    with_roll = True
    t0 = systime()
    tilt_pv = '13IDA:DAC1_7.VAL'
    roll_pv = '13IDA:DAC1_8.VAL'
    i0_pv   = '13IDE:IP330_1.VAL'
    sum_pv  = '13IDA:QE2:SumAll:MeanValue_RBV'


    if enable_fb_pitch is None:
        enable_fb_pitch = caget('13IDE:En:Energy') < 3000.0
    #endif

    caput('13XRM:edb:use_fb', 0)
    caput('13IDA:efast_pitch_pid.FBON', 0)
    caput('13IDA:efast_roll_pid.FBON', 0)

    i0_minval = 0.1   # expected smallest I0 Voltage

    # stop, restart Quad Electrometer
    caput('13IDA:QE2:Acquire', 0) ;     sleep(0.25)
    caput('13IDA:QE2:Acquire', 1) ;     sleep(0.25)
    caput('13IDA:QE2:ReadData.PROC', 1)

    # find best tilt value with BPM sum
    out = find_max_intensity(sum_pv, tilt_pv, linspace(-2.5, 2.5, 51))
    if get_dbinfo('request_abort', as_bool=True): return
    print '  Best Pitch (BPM): %.3f at %.3f ' % (out)

    # find best tilt value with IO
    out = find_max_intensity(i0_pv, tilt_pv, linspace(-1.0, 1.0, 51))
    if get_dbinfo('request_abort', as_bool=True): return
    print '  Best Pitch (I0): %.3f at %.3f ' % (out)

    # find best roll with I0
    if with_roll:
        out = find_max_intensity(i0_pv, roll_pv, linspace(-3.5, 3.5, 71))
        if get_dbinfo('request_abort', as_bool=True): return
        print '  Roll first pass %.3f at %.3f ' % (out)
        if out[0] > 0.002:
            out = find_max_intensity(i0_pv, roll_pv, linspace(1, -1, 51))
            if get_dbinfo('request_abort', as_bool=True): return
        #endif
        print '  Best Roll %.3f at %.3f ' % (out)
    #endif

    sleep(0.5)
    # re-find best tilt value, now using I0
    out = find_max_intensity(i0_pv, tilt_pv, linspace(-1.5, 1.5, 101))
    if get_dbinfo('request_abort', as_bool=True): return
    print '  Final Best Pitch: %.3f at %.3f ' % (out)
    sleep(0.5)
    caput('13IDA:QE2:ComputePosOffsetX.PROC', 1, wait=True)
    caput('13IDA:QE2:ComputePosOffsetY.PROC', 1, wait=True)
    sleep(0.5)
    caput('13IDA:efast_pitch_pid.FBON', 0)
    if enable_fb_roll:
        caput('13IDA:efast_roll_pid.FBON', 1)
    #endif

    if enable_fb_pitch:
        sleep(3.0)
        caput('13XRM:edb:use_fb', 1)
    #endif

    print 'Set Mono tilt done (%.2f seconds)' % (systime()-t0)
#enddef
