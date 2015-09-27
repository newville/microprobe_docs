##
## Macros for X-ray Diffraction
##
def save_xrd(name, t=10, ext=None, prefix='13PEL1:', timeout=60.0):
   # save_xrd_marccd(name, t=t, ext=ext, prefix=prefix)
   save_xrd_pe(name, t=t, ext=ext, prefix=prefix)
#enddef


def save_xrd_pe(name, t=10, ext=None, prefix='13PEL1:', timeout=60.0):
    """Save XRD image from Perkin Elmer camera to file

    use prefix=dp_pe2: for detector pool camera!

    Parameters
    ----------
    name:     string for sample name
    t:        exposure time in seconds (default = 10)
    ext:      number for file extension (default = 1)
    prefix:   Camera PV prefix ('13PE1:')

    Examples
    --------
    save_xrd('CeO2', t=20)
    """
    # prefix='dp_pe2:'

    # save shutter mode, disable shutter for now
    shutter_mode = caget(prefix+'cam1:ShutterMode')
    caput(prefix+'cam1:ShutterMode', 0)
    sleep(0.1)

    caput(prefix+'cam1:Acquire', 0)
    sleep(0.1)
    print("Save XRD...")
    caput(prefix+'TIFF1:EnableCallbacks', 0)
    caput(prefix+'TIFF1:AutoSave',        0)
    caput(prefix+'TIFF1:AutoIncrement',   1)
    caput(prefix+'TIFF1:FileName',     name)
    if ext is not None:
        caput(prefix+'TIFF1:FileNumber',    ext)
    #endif
    caput(prefix+'TIFF1:EnableCallbacks', 1)
    caput(prefix+'cam1:ImageMode',        3)

    sleep(0.1)
    acq_time =caget(prefix+'cam1:AcquireTime')

    numimages = int(t*1.0/acq_time)
    caput(prefix+'cam1:NumImages', numimages)

    # expose
    caput(prefix+'cam1:Acquire', 1)
    sleep(0.5 + max(0.5, 0.5*t))
    t0 = clock()
    print('Wait for Acquire ... ')
    while ((1 == caget(prefix+'cam1:Acquire')) and
            (clock()-t0 < timeout)):
        sleep(0.25)
    #endwhile
    print('Done!')
    sleep(0.1)

    # clean up, returning to short dwell time
    caput(prefix+'TIFF1:WriteFile',       1)
    caput(prefix+'TIFF1:EnableCallbacks', 0)
    sleep(0.5)
    caput(prefix+'cam1:ImageMode', 2)
    caput(prefix+'cam1:ShutterMode', shutter_mode)
    sleep(0.5)
    caput(prefix+'cam1:Acquire', 1)
#enddef

def save_xrd_marccd(name, t=10, ext=None, prefix='13MARCCD1:', timeout=60.0):
    """Save XRD image from MARCCD camera to file

    Parameters
    ----------
    name:     string for sample name
    t:        exposure time in seconds (default = 10)
    ext:      number for file extension (default = 1)
    prefix:   Camera PV prefix ('13MARCCD1:')

    Examples
    --------
    save_xrd('CeO2', t=20)
    """
    start_time = time()

    # save shutter mode, disable shutter for now
    shutter_mode = caget(prefix+'cam1:ShutterMode')
    # NOTE: Need to start acquisition with the shutter
    # having been closed for awhile
    # using the SSA H Width as shutter we want
    caput(prefix+'cam1:ShutterControl', 0)
    sleep(5.0)
    print 'Shutter really, really closed'
    caput(prefix+'cam1:FrameType', 0)
    caput(prefix+'cam1:ShutterMode', 1)
    caput(prefix+'cam1:ImageMode', 0)
    caput(prefix+'cam1:AutoSave',       1)
    caput(prefix+'cam1:AutoIncrement',  1)
    caput(prefix+'cam1:FileName',    name)
    if ext is not None:
        caput(prefix+'cam1:FileNumber',    ext)
    #endif
    caput(prefix+'cam1:AcquireTime', t)

    sleep(0.1)

    # expose
    caput(prefix+'cam1:Acquire', 1)
    sleep(1.0 + max(1.0, t))
    t0 = clock()
    print('Wait for Acquire ... ')
    while ((1 == caget(prefix+'cam1:Acquire')) and
            (clock()-t0 < timeout)):
        sleep(0.2533)
    #endwhile

    print('Acquire Done! %.3f sec' % (time()-start_time))
    sleep(2.0)
    caput(prefix+'cam1:ShutterControl', 1)
#enddef


def xrd_bgr(prefix='13MARCCD1:', timeout=120.0):
    """XRD Background"""
    caput(prefix+'cam1:ShutterControl', 0)
    caput(prefix+'cam1:FrameType', 1)
    sleep(0.1)

    caput(prefix+'cam1:Acquire', 1)
    sleep(3)
    t0 = clock()
    print('Wait for Acquire ... ')
    while ((1 == caget(prefix+'cam1:Acquire')) and
            (clock()-t0 < timeout)):
        sleep(0.25)
    #endwhile
    sleep(2.0)
#enddef
