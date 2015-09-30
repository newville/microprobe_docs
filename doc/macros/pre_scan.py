"""
The function `pre_scan_command` is run automatically
just before many of the internal scanning commands:

 * before each 1-d scan, including XAFS Scans
 * before each 2-d mesh scan,
 * before each row of a 2-d slew scan.

"""

def pre_scan_command(scan=None):
    """
    function run prior to each internal scanning command

    This can be used to customize checks for intensity, etc.

    Note:
      1. Consult Matt and Tony before modifying!
      2. Most detectors have their own `pre_scan` and
         `post_scan` functions, too, and so shouldn't need
         to be put in proper modes, here. But, those settings
         can be tweaked here, as this command is actually
         run after all the detector `pre_scan` commands.

    """
    print 'This is pre_scan_command(), last updated 24-Sep-2015'
    sleep(1)

    # Step 1: restart QE2
    caput('13IDA:QE2:Acquire', 0)
    sleep(0.5)
    caput('13IDA:QE2:Acquire', 1)

    i0_flux = float(caget('13XRM:ION:FluxOut'))
    i0_llim = float(caget('13XRM:ION:FluxLowLimit'))

    # Step 2: if flux is low, wait, tweak energy
    if (i0_flux < i0_llim):
        t0 = systime()
        energy_tweaked = False
        energy = caget('13IDE:En:Energy')
        while i0_flux < i0_llim and (systime()-t0) < 30.0:
            sleep(0.250)
            i0_flux = float(caget('13XRM:ION:FluxOut'))
            i0_llim = float(caget('13XRM:ION:FluxLowLimit'))
            # may need to tweak the energy (ID may be wrong)
            if (systime() - t0) > 15.0 and not energy_tweaked:
                energy_tweaked = True
                caput('13IDE:En:Energy', energy + 0.1)
            #endif
            if check_scan_abort():  return
        #endwhile
    #endif

    # Step 3: if flux is still low, set mono tilt
    if (i0_flux < i0_llim):
        print("I0 Flux = %.4g too low, setting mono tilt" % i0_flux)
        set_mono_tilt()
        if check_scan_abort():  return
    #endif

    # Step 4: longer wait, as if beam dumped
    WAIT_TIME = 4*3600.0

    i0_flux = float(caget('13XRM:ION:FluxOut'))
    i0_llim = float(caget('13XRM:ION:FluxLowLimit'))
    t0 = t0en = systime()
    energy = caget('13IDE:En:Energy')
    en_off = 0

    if (i0_flux < i0_llim):
        print(" I0 flux too low, waiting (hit Abort to cancel)")
    #endif
    while i0_flux < i0_llim and systime()-t0 < WAIT_TIME:
        sleep(1.0)
        i0_flux = float(caget('13XRM:ION:FluxOut'))
        i0_llim = float(caget('13XRM:ION:FluxLowLimit'))
        # may need to tweak the energy (ID may be wrong)
        if (systime() - t0en) > 120.0:
            t0en = systime()
            en_off  += 0.1
            if en_off > 1.02: en_off = -1.0
            caput('13IDE:En:Energy', energy + en_off)
        #endif
        if check_scan_abort():  return
    #endwhile
    return None
#enddef
