"""
Commands for X-ray Diffraction

Note that an XRD camera must be installed!
"""

def setup_epics_shutter(prefix='13MARCCD4:'):
    """
    Setup Epics shutter for CCD camera
       open /close pv = 13IDA:m70.VAL (SSA H WID)
       open val =  0.080, close val = -0.020
    """
    caput(prefix+'cam1:ShutterOpenEPICS.OUT',   '13IDA:m70.VAL')
    caput(prefix+'cam1:ShutterCloseEPICS.OUT',  '13IDA:m70.VAL')
    caput(prefix+'cam1:ShutterOpenEPICS.OCAL',  '0.080')
    caput(prefix+'cam1:ShutterCloseEPICS.OCAL', '-0.020')
    caput(prefix+'cam1:ShutterOpenDelay',        1.50)
    caput(prefix+'cam1:ShutterCloseDelay',       0.0)
    caput(prefix+'cam1:ShutterMode',             1)
#enddef

def clear_epics_shutter(prefix='13MARCCD4:'):
    """
    Clear Epics shutter PV for CCD camera
    """
    caput(prefix+'cam1:ShutterOpenEPICS.OUT',   '')
    caput(prefix+'cam1:ShutterCloseEPICS.OUT',  '')
    caput(prefix+'cam1:ShutterOpenEPICS.OCAL',  '0')
    caput(prefix+'cam1:ShutterCloseEPICS.OCAL', '0')
    caput(prefix+'cam1:ShutterOpenDelay',        0.1)
    caput(prefix+'cam1:ShutterCloseDelay',       0.1)
    caput(prefix+'cam1:ShutterMode',             0)
#enddef

def close_ccd_shutter():
    caput('13IDA:m70.VAL', -0.025, wait=True)
    sleep(1.0)
#enddef

def open_ccd_shutter():
    caput('13IDA:m70.VAL', 0.080, wait=True)
    sleep(1.0)
#enddef

def save_xrd(name, t=10, ext=None, prefix='13PEL1:', timeout=60.0):
##  prefix='13PEL1:' prefix='13MARCCD1:'
    """
    Save XRD image from XRD camera.

    Parameters:
        name (string):  name of datafile
        t (float):   exposure time in seconds [default= 10]
        ext (int or None): number for file extension
            if left as None, the extension will be auto-incremented.
        prefix (string):   PV prefix for areaDetector camera ['13PE1:']
        timeout (float): maximumn time in seconds to wait
            for image to be saved [60]

    Examples:
        save_xrd('CeO2', t=20)

    Note:
        calls one of `save_xrd_marccd` or `save_xrd_pe`

    See Also:
       `save_xrd_marccd`, `save_xrd_pe`

    """
    if 'mar' in prefix.lower():
        save_xrd_marccd(name, t=t, ext=ext, prefix=prefix)
    else:
        save_xrd_pe(name, t=t, ext=ext, prefix=prefix)
    #endif
#enddef


def save_xrd_pe(name, t=10, ext=None, prefix='13PEL1:', timeout=60.0):
    """
    Save XRD image from Perkin-Elmer camera.

    Parameters:
        name (string):  name of datafile
        t (float):   exposure time in seconds [default= 10]
        ext (int or None): number for file extension
            if left as None, the extension will be auto-incremented.
        prefix (string):   PV prefix for areaDetector camera ['13PE1:']
        timeout (float): maximumn time in seconds to wait
            for image to be saved [60]

    Examples:
        save_xrd_pe('CeO2', t=20)

    Note:
        detector pool PE detector has prefix like 'dp_pe2:'
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

    sleep(0.5)
    acq_time =caget(prefix+'cam1:AcquireTime')

    numimages = int(t*1.0/acq_time)
    caput(prefix+'cam1:NumImages', numimages)

    # expose
    caput(prefix+'cam1:Acquire', 1)
    sleep(0.5 + max(0.5, 0.5*t))
    t0 = clock()
    nrequested = caget(prefix+'cam1:NumImages')
    print('Wait for Acquire ... %i' % nrequested)

    while ((1 == caget(prefix+'cam1:Acquire')) and
            (clock()-t0 < timeout)):
        sleep(0.25)

    #endwhile
    print('Acquire Done, writing file %s' % name)
    sleep(0.1)

    # clean up, returning to short dwell time
    caput(prefix+'TIFF1:WriteFile',       1)
    caput(prefix+'TIFF1:EnableCallbacks', 0)
    sleep(0.5)

    caput(prefix+'cam1:ImageMode', 2)
    caput(prefix+'cam1:ShutterMode', shutter_mode)
    sleep(0.5)
    caput(prefix+'cam1:Acquire', 1)
    sleep(1.5)
#enddef

def save_xrd_marccd(name, t=10, ext=None, prefix='13MARCCD4:', timeout=60.0):
    """
    save XRD image from MARCCD (Rayonix 165) camera to file

    Parameters:
        name (string):  name of datafile
        t (float):   exposure time in seconds [default= 10]
        ext (int or None): number for file extension
            if left as None, the extension will be auto-incremented.
        prefix (string):   PV prefix for areaDetector camera ['13MARCCD1:']
        timeout (float): maximumn time in seconds to wait
            for image to be saved [60]

    Examples:
        save_xrd_marccd('CeO2', t=20)

    Note:
        The marccd requires the Epics Shutter to be set up correctly.

    """
    start_time = systime()

    # save shutter mode, disable shutter for now
    shutter_mode = caget(prefix+'cam1:ShutterMode')


    # NOTE: Need to start acquisition with the shutter
    # having been closed for awhile
    # using the SSA H Width as shutter we want
    # NOTE: Need to start acquisition with the shutter
    # having been closed for awhile
    # using the SSA H Width as shutter we want

    caput(prefix+'cam1:ShutterControl', 0)
    close_ccd_shutter()

    caput(prefix+'cam1:FrameType', 0)
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
    t0 = systime()
    print('Wait for Acquire ... ')
    while ((1 == caget(prefix+'cam1:Acquire')) and
            (clock()-t0 < timeout)):
        sleep(0.25)
    #endwhile

    fname = caget(prefix+'cam1:FullFileName_RBV', as_string=True)
    print('Acquire Done! %.3f sec' % (systime()-start_time))
    print('Wrote %s' % fname)
    sleep(1.0)
    caput(prefix+'cam1:ShutterControl', 1)
#enddef


def xrd_at(posname,  t):
    move_samplestage(posname, wait=True)
    save_xrd(posname, t=t, ext=1)
#enddef


def xrd_bgr_marccd(prefix='13MARCCD4:', timeout=120.0):
    """
    collect XRD Background for marccd

    Parameters:
        prefix (string): PV prefix for camera ['13MARCCD1:']
        timeout (float): maximum time to wait [120]

    """
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


def xrd_bgr(prefix='13PEL1:'):
    """
    collect XRD Background for Perkin Elmer

    Parameters:
        prefix (string): PV prefix for camera ['13MARCCD1:']
    
    """

    caput(prefix+'cam1:ShutterMode', 1)
    immode = caget(prefix+'cam1:ImageMode')
    caput(prefix+'cam1:ImageMode', 1)
    caput(prefix+'cam1:ShutterControl', 0)
    sleep(3)
    caput(prefix+'cam1:PEAcquireOffset', 1)
    sleep(5)

    caput(prefix+'cam1:ShutterControl', 1)
    caput(prefix+'cam1:ImageMode', immode)
    caput(prefix+'cam1:Acquire', 1)
    sleep(2.0)
#enddef