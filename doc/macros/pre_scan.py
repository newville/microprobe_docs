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
    print 'Pre_scan_command() from 1-March-2016'
    sleep(0.1)

    # Step 0: restart QE2
    caput('13IDA:QE2:Acquire', 0)
    sleep(0.25)
    caput('13IDA:QE2:Acquire', 1)
    
    try:
      fluxlow = float(caget('13XRM:ION:FluxLowLimit'))
    except:
      fluxlow = 1.e7
    #endtry
    if fluxlow < 200: 
        print("not waiting for shutter")
        return
    #endif
     
    # Step 1: wait up to 12 hours for shutters to open
    #  try opening shutters every 15 minutes
    shutter_status = (caget('13IDA:eps_mbbi25'), caget('13IDA:eps_mbbi27'))
    # print  "Shutter: ", shutter_status
    if shutter_status != (1, 1): 
        print 'Waiting for shutters to open'
        t0 = systime()
        while shutter_status != (1, 1) and (systime()-t0 < 12*3600.0):
            shutter_status = (caget('13IDA:eps_mbbi25'), caget('13IDA:eps_mbbi27'))
            sleep(1.0)
            if int(systime()) % 900 < 10:
                caput('13IDA:OpenFEShutter.PROC', 1)
                caput('13IDA:OpenEShutter.PROC',  1)
                sleep(10)
            #endif
            if check_scan_abort():  return
        #endwhile			
    #endif

    # Step 3: if flux is low, wait, tweak energy
    i0_flux = float(caget('13XRM:ION:FluxOut'))
    i0_llim = float(caget('13XRM:ION:FluxLowLimit'))
    if (i0_flux < i0_llim):
        print(" Waiting for I0 flux.")
        t0 = systime()
        energy_tweaked = False
        energy = caget('13IDE:En:Energy')
        while i0_flux < i0_llim and (systime()-t0) < 600.0:
            sleep(1)
            i0_flux = float(caget('13XRM:ION:FluxOut'))
            i0_llim = float(caget('13XRM:ION:FluxLowLimit'))
            if int(systime()) % 30 < 5:
                caput('13IDE:En:Energy', energy + 0.1)
                sleep(5)
            #endif
            if check_scan_abort():  return
        #endwhile
    #endif

    # Step 4: if flux is still low, set mono tilt
    if (i0_flux < i0_llim):
        print("I0 Flux = %.4g too low, setting mono tilt" % i0_flux)
        set_mono_tilt()
        if check_scan_abort():  return
    #endif

    # Step 5: if flux is still too low, wait another hour, 
    # hoping for operator intervention
    i0_flux = float(caget('13XRM:ION:FluxOut'))
    i0_llim = float(caget('13XRM:ION:FluxLowLimit'))
    energy = caget('13IDE:En:Energy')
    en_off = 0
    t0 = systime()

    if (i0_flux < i0_llim):
        print(" I0 flux too low, waiting for 1 hour (do something or hit Abort to cancel)")
    #endif
    while i0_flux < i0_llim and systime()-t0 < 3600.0:
        i0_flux = float(caget('13XRM:ION:FluxOut'))
        i0_llim = float(caget('13XRM:ION:FluxLowLimit'))
        sleep(1.0)
        # may need to tweak the energy (ID may be wrong)
        if systime() % 120.0 < 5:
            en_off  += 0.1
            if en_off > 2.02: en_off = -2.0
            caput('13IDE:En:Energy', energy + en_off)
            sleep(5)
        #endif
        if check_scan_abort():  return
    #endwhile
    
    #print 'Done with pre-scan!'
    return None
#enddef
