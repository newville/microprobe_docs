##
## Macros for scanning
##

def pre_scan_command(scan=None):
  """function run prior to each real scan"""
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

def pos_scan(pos, scanfile, datafile=None, number=1):
    "pos_scan('MySample', 'Fe_XANES', number=3) "
    move_samplestage(pos, wait=True)
    sleep(1.0)
    if datafile is None:
        datafile = '%s_%s.001' % (scanfile, pos)
    #endif
    do_scan(scanfile,  filename=datafile, nscans=number)
#enddef

def pos_map(pos, mapname):
    "pos_map('MySample', 'MyMap')"
    move_samplestage(pos, wait=True)
    sleep(1.0)
    datafile = '%s_%s.001' % (mapname, pos)
    do_slewscan(mapname, filename=datafile)
#enddef


def xafs_grid(scan_name, name=None, xstart=0, xstop=0.1, xstep=0.001, ystart=0, ystop=0.1, ystep=0.001):
    """ do xafs scan at each point in a grid
    """
    # move_samplestage(pos_name, wait=True)
    #sleep(1.0)

    datafile= scan_name
    if name is not None:
        datafile = '%s_%s' % (name, scan_name)
    #endif

    # motor name:
    xmotor = '13XRM:m1.VAL'
    ymotor = '13XRM:m2.VAL'

    xvals = linspace(xstart, xstop, (abs(xstart-xstop)+xstep/2.0)/abs(xstep))
    yvals = linspace(ystart, ystop, (abs(ystart-ystop)+ystep/2.0)/abs(ystep))
    for iy, yval in enumerate(yvals):
        caput(ymotor, yval, wait=True)
        for ix, xval in enumerate(xvals):
            caput(xmotor, xval, wait=True)
            do_scan(scan_name,  filename='%s_x%iy%i.001' % (datafile, ix+1, iy+1))
            if check_scan_abort():  return
        #endfor
    #endfor
#enddef


def loop_map(pos_name, map_name, datafile=None, motor='y', start=0, stop=0.1, step=0.001):
    """ loop_map(pos_name, map_name, start=0, stop=0.1, step=0.001)
    """
    print 'Move Sample Stage ', pos_name
    move_samplestage(pos_name, wait=True)
    sleep(1.0)
    if datafile is None:
        datafile = '%s_%s' % (pos_name, map_name)
    #endif
    # resolve motor name:
    if motor == 'x':  motor = '13XRM:m1.VAL'
    if motor == 'y':  motor = '13XRM:m2.VAL'
    if motor == 'th': motor = '13XRM:m3.VAL'

    step = abs(step)
    values = linspace(start, stop, (abs(start-stop)+step)/step)
    for i, val in enumerate(values):
        print 'move motor: ', motor, val
        caput(motor, val, wait=True)
        do_slewscan(map_name,  filename='%s_%i' % (datafile, i))
        if check_scan_abort():  return
    #endfor
#enddef


def line_scan(pos, scanfile, datafile=None, motor='x', start=0, stop=0.1, step=0.001, nscans=1):
    """line_scan(position_name, scan_name, start=0, stop=0.1, step=0.001)
    """
    # print 'Move Sample Stage ', pos
    move_samplestage(pos, wait=True)
    sleep(1.0)
    if datafile is None:
        datafile = '%s_%s' % (scanfile, pos)
    #endif

    # resolve motor name:
    motor_dir=motor
    if motor == 'x':  motor = '13XRM:m1.VAL'
    if motor == 'y':  motor = '13XRM:m2.VAL'
    if motor == 'th': motor = '13XRM:m3.VAL'

    basename = datafile
    step = abs(step)
    xvalues = linspace(start, stop, (abs(start-stop)+step)/step)
    for i, xval in enumerate(xvalues):
        print 'move motor ', motor, xval
        caput(motor, xval, wait=True)
        if i < 10 : datafile = '%s_%s_pos0%i.001' % (basename, motor_dir, i)
        if i >= 10 : datafile = '%s_%s_pos%i.001' % (basename, motor_dir, i)
        do_scan(scanfile,  filename=datafile, nscans=nscans)
        if check_scan_abort():  return
    #endfor
#enddef

def redox_map(pos, scan, energies=[5460, 5467.5, 5469, 5485.9, 5493.3, 5600], datafile=None):
    """ redox map: move to a position, repeat map at multiple energies

   redox_map(pos, scan, energies=[5450, 5465, 5500])

    arguments
    ---------
      pos       position name
      scan      scan name for map
      energies  list of energies to map at
    """
    print 'Move Sample Stage ', pos
    move_samplestage(pos, wait=True)
    sleep(0.5)
    if datafile is None:
        datafile = '%s_%s' % (scan, pos)
    #endif

    for en in energies:
        move_energy(en)
        dfile = '%s_%.1feV.001' % (datafile, en)
        do_scan(scan,  filename=dfile)
        if check_scan_abort():  return
    #endfor
#enddef


def xrd_map(name, t=5, xstart=0, xstop=0.1, xstep=0.001, ystart=0, ystop=0.1, ystep=0.001):
    """
    xrd at each point in a rectangular grid
    """
    xstep = abs(xstep)
    ystep = abs(ystep)
    xvalues = linspace(xstart, xstop, (abs(xstart-xstop)+xstep*1.1)/xstep)
    yvalues = linspace(ystart, ystop, (abs(ystart-ystop)+ystep*1.1)/ystep)
    for iy, y in enumerate(yvalues):
        caput('13XRM:m2.VAL', y, wait=True)
        xrd_bgr()
        fname = name + '_%i' % (iy+1)
        caput('13MARCCD1:cam1:FileNumber', 1)
        for x in xvalues:
           print 'move x ', x
           caput('13XRM:m1.VAL', x, wait=True)
           save_xrd(fname, t=t)
           if check_scan_abort():  return
        #endfor
    #endfor
    sleep(1.0)
#enddef
