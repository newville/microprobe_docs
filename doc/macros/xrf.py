def save_xrf(filename, t=15.0):
    """
    Save XRF spectrum

    Parameters:
        name (string):  name of datafile
        t (float):   exposure time in seconds [default= 10]

    Examples:
        save_xrf('mysample', t=20)

    """
    t = t*1.0

    prefix = '13QX4:'

    det = epics_xspress3(prefix=prefix, nmca=4)

    det.set_dwelltime(t)
    sleep(0.25)
    det.start()

    env = []
    envfile = open('/cars5/Data/xas_user/scan_config/13ide/IDE_QX4_ENV.DAT', 'r')
    for line in envfile.readlines():
        if len(line)<  3: continue
        line = line[:-1]
        pvname, desc = line.split(' ', 1)
        desc = desc.strip()
        desc = desc.replace('\r', '').replace('\n', '')
        val = caget(pvname)
        env.append((pvname, val, desc))
    #endfor
    envfile.close()

    t0 = systime()
    sleep(2.0)
    counting = True
    while counting:
        counting = (caget('13QX4:DetectorState_RBV') != 0)
        if systime() - t0 > (t+30): counting = False
        # print 'Hello ', systime() - t0
    #endwhile

    det.save_mcafile(filename, environ=env)
    print "Wrote ", filename

#enddef
