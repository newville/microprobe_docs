"""
Scanning Commands

    pos_scan: move to a Named Position, run a Scan
    pos_map

"""

from common import check_scan_abort
from energy import move_energy
from samplestage import move_samplestage

def pos_scan(posname, scanname, datafile=None, number=1):
    """
    move sample to a Named Position from SampleStage Positions list
    and run a scan defined from EpicsScan

    Parameters:
        posname  (string): Name of Position from SampleStage position list.
        scanname (string): Name of Scan, as defined and saved from EpicsScan.
        datafile (string or None): Name of datafile to write [default=None]
            if None, datafile will be '<scanname>_<pos>.001'
        number (integer): number of repeats of scan to do [default=1]

    Example:
       pos_scan('MySample', 'Fe_XANES', number=3)

    """
    move_samplestage(posname, wait=True)
    sleep(1.0)
    if datafile is None:
        datafile = '%s_%s.001' % (scanname, posname)
    #endif
    do_scan(scanname,  filename=datafile, nscans=number)
#enddef

def pos_map(posname, scanname):
    """
    move to a Named Position from SampleStage Positions list
    and run a slewscan map named in EpicsScan

    Parameters:
        posname (string):  Name of Position from SampleStage position list.
        scanname (string): Name of Scan, as defined and saved from EpicsScan.

    Example:
       pos_map('MySample', 'MyMap')
    """

    move_samplestage(posname, wait=True)
    sleep(1.0)
    datafile = '%s_%s.001' % (scanname, posname)
    do_slewscan(scanname, filename=datafile)
#enddef


def _getPV(mname):
    """
    get PV name for a motor description.
    expected to be used internally.

    Parameters:
        mname (string): name of motor or other PV that can be scanned

    Returns:
        PVname (string) for motor, or None if not found in known names

    Example:
        xpv = _get_motorPV('x')

    Note:
        known names are:
           'x' or 'finex' : sample fine X stage
           'y' or 'finey' : sample fine Y stage
           'z'            : sample Z (focus) stage
           'coarsex'      : sample coarse X stage
           'coarsey'      : sample coarse Y stage
           'energy'       : monochromator energy
    """

    known = {'x':       '13XRM:m1.VAL',    'finex':   '13XRM:m1.VAL',
             'y':       '13XRM:m2.VAL',    'finey':   '13XRM:m2.VAL',
             'z':       '13XRM:m5.VAL',    'theta':   '13XRM:m3.VAL',
             'coarsex': '13XRM:m4.VAL',    'coarsey': '13XRM:m6.VAL',
             'energy':  '13IDE:En:Energy',
             }
    return known.get(mname.lower(), None)
#enddef

def _scanloop(scanname, datafile, motorname, vals, number=1):
    """
    run a named scan at each point for a named motor.
    expected to be used internally.

    Parameters:
        scanname (string): name of scan
        datafile (string): name of datafile (must be given)
        motorname (string): name of motor
        vals (list or array of floats): motor values at which to do scan.
        number(int): number of scan repeats at each point

    Example:
        _scanloop('Fe_XAFS', 'sample1_', 'x', [-0.1, 0.0, 0.1])

    Note:
        output files will named <scanname>_<datafile>_<motorname>I.001
        where I will increment 1, 2, 3, .. number of points in vals.
        For the above example, the files will be named
            'Fe_XAFS_sample1_x1.001',
            'Fe_XAFS_sample1_x2.001',
            'Fe_XAFS_sample1_x3.001'
    """
    motor = _getPV(motorname)
    if motor is None:
        print("Error: cannot find motor named '%s'" % motorname)
        return
    #endif
    filename = '%s_%s_%s.001' % (scanname, datafile, motorname)
    for i, val in enumerate(vals):
        caput(motor, val, wait=True)
        do_scan(scanname,  filename=filename, nscans=number)
        if check_scan_abort(): return
    #endfor
#enddef

def line_scan(scanname, datafile, motor='x',
              start=0, stop=0.1, step=0.001, number=1):
    """
    run a named scan (or map) at each point in along a line

    Parameters:
        scanname (string): name of scan
        datafile (string): name for datafile
        motor (string): name of motor to move ['x']
        start (float): starting motor value [0]
        stop (float): ending motor value [0.100]
        step (float): step size for motor [0.001]
        number(int): number of scan repeats at each point
    Example:
        line_scan('Fe_XAFS', 'sample1', motor='x', start=0, stop=0.05, step=0.005, number=2)

    Note:
       output files will named `<scanname>_<datafile>_<x>I.001`  where I will
       increment 1, 2, 3, and so on.

       For the example above, the files will be named 'Fe_XAFS_sample1_x1.001',
       'Fe_XAFS_sample1_x1.002', 'Fe_XAFS_sample1_x2.001', 'Fe_XAFS_sample1_x2.002',
       'Fe_XAFS_sample1_x3.001', 'Fe_XAFS_sample1_x2.002', and so on.

    See Also:
       grid_scan

    """
    vals = linspace(start, stop, (abs(start-stop)+0.2*step)/abs(step))

    _scanloop(scanname, datafile, motor, vals, number=number)
#enddef


def grid_scan(scanname, datafile, x='x', y='y',
              xstart=0, xstop=0.1, xstep=0.001,
              ystart=0, ystop=0.1, ystep=0.001):
    """
    run a named scan (or map) at each point in an x, y grid

    Parameters:
        scanname (string): name of scan
        datafile (string): name for datafile
        x (string): name of X motor (inner loop) ['x']
        y (string): name of Y motor (outer loop) ['y']
        xstart (float): starting X value [0]
        xstop (float): ending X value [0.100]
        xstep (float): step size for X value [0.001]
        ystart (float): starting Y value [0]
        ystop (float): ending Y value [0.100]
        ystep (float): step size for Y value [0.001]

    Example:
        grid_scan('Fe_XAFS', 'sample1', y='theta', xstart=0, xstop=0.05, xstep=0.005,
                   ystart=0, ystop=10, ystep=1)

    Note:
        output files will named <scanname>_<datafile>_<y>I_<x>J.001
        where I and J will increment 1, 2, 3, ...
        For the above example, the files will be named
        'Fe_XAFS_sample1_theta1_x1.001',
        'Fe_XAFS_sample1_theta1_x2.001',
        'Fe_XAFS_sample1_theta1_x3.001', and so on

    See Also:
        line_scan, grid_xrd

    """
    yname = y
    xname = x

    xvals = linspace(xstart, xstop, (abs(xstart-xstop)+0.2*xstep)/abs(xstep))
    yvals = linspace(ystart, ystop, (abs(ystart-ystop)+0.2*ystep)/abs(ystep))

    ymotor = _getPV(yname)
    if ymotor is None:
        print("Error: cannot find motor named '%s'" % yname)
        return
    #endif

    for iy, yval in enumerate(yvals):
        caput(ymotor, yval, wait=True)
        ydatafile = "%s_%s%i" % (datafile, yname, iy+1)
        _scanloop(scanname, ydatafile, xname, xvals)
        if check_scan_abort():  return
    #endfor
#enddef

def redox_map(scanname, datafile=None,
              energies=[5460, 5467.5, 5469, 5485.9, 5493.3, 5600]):
    """
    repeat a scan or map at multiple energies

    Parameters:
        scanname (string):  scan name
        datafile (string or None): name for datafile
        energies (list of floats):   list of energies (in eV) to run map scan at

    Example:
       redox_map('MyMap', 'sampleX', energies=[5450, 5465, 5500])

    Note:
        output files will named <scanname>_<energy>eV.001
        for the example above, the files will be named
        'MyMap_sampleX_5450.0eV.001',
        'MyMap_sampleX_5465.0eV.001',
        'MyMap_sampleX_5500.0eV.001',

    """
    if datafile is None:
        datafile = scanname
    #endif

    for en in energies:
        move_energy(en)
        dfile = '%s_%.1feV.001' % (datafile, en)
        do_scan(scan,  filename=dfile)
        if check_scan_abort():  return
    #endfor
#enddef


def grid_xrd(datafile, t=5, x='x', y='y',
             xstart=0, xstop=0.1, xstep=0.001,
             ystart=0, ystop=0.1, ystep=0.001, bgr_per_row=False):
    """
    collect an XRD image at each point in an x, y grid
    running save_xrd() at each point in the grid

    Parameters:
        datafile (string): name for datafile
        t (float): exposure time per pixel
        x (string): name of X motor (inner loop) ['x']
        y (string): name of Y motor (outer loop) ['y']
        xstart (float): starting X value [0]
        xstop (float): ending X value [0.100]
        xstep (float): step size for X value [0.001]
        ystart (float): starting Y value [0]
        ystop (float): ending Y value [0.100]
        ystep (float): step size for Y value [0.001]
        bgr_per_row (True or False): whether to collec xrd_bgr()
            at the beginning of each row.

    Example:
        grid_xrd('MySample', xstart=0, xstop=0.05, xstep=0.005,
                  ystart=0, ystop=10, ystep=1)

    Note:
        output files will named <scanname>_<datafile>_<y>I_<x>J.001
        where I and J will increment 1, 2, 3, and so on.
        For the above example, the files will be named
        'MySample_y1_x1.001', 'MySample_y1_x2.001', and so on

    See Also:
        save_xrd, xrd_bgr

    """

    yname = y
    xname = x

    xvals = linspace(xstart, xstop, (abs(xstart-xstop)+0.2*xstep)/abs(xstep))
    yvals = linspace(ystart, ystop, (abs(ystart-ystop)+0.2*ystep)/abs(ystep))

    ymotor = _getPV(yname)
    if ymotor is None:
        print("Error: cannot find motor named '%s'" % yname)
        return
    #endif

    for iy, yval in enumerate(yvals):
        caput(ymotor, yval, wait=True)
        if bgr_per_row: xrd_bgr()
        ydatafile = "%s_%s%i" % (datafile, yname, iy+1)
        for ix, xval in enumerate(xvals):
           caput(xmotor, xval, wait=True)
           fname = ydatafile + '_%s%i' % (xname, ix+1)
           save_xrd(fname, t=t, ext=1)
           if check_scan_abort():  return
        #endfor
    #endfor
#enddef
