def move_fine(x=None, y=None):
    "move fine stages to x, y values"
    if x is not None:
       caput('13XRM:m1.VAL', x)
    #endif
    if y is not None:
       caput('13XRM:m2.VAL', y)
    #endif
#enddef


def move_samplestage(position, instrument='IDE_SampleStage', wait=True, timeout=60):
    """move Sample Stage to named position

    Parameters
    ----------
    position:   string, name of sample stage position
    instrument: string, name of instrument ['IDE_SampleStage']
    wait:       True/False, whether to wait for move to complete [True]
    timeout:    maximum time (seconds) to wait when wait=True [60.0]

    Examples
    --------
      move_samplestage('Sample 1')
    """
    idb = _scan._instdb
    thispos = idb.get_position(instrument, position)
    if thispos is None:
       print(" Could not find position '%s'" % position)
    else:
       idb.restore_position(instrument, position, wait=wait, timeout=timeout)
    #endif
#enddef
