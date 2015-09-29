def move_fine(x=None, y=None):
    """
    Move fine stages to x, y values

    Parameters:
        x (float or None): value for (fine)X  position.
        y (float or None): value for (fine)Y  position.

    Examples:
        move_fine(0.220, -0.380)

        move_fine(y=0.0)

    Notes:
        if a value is None, that stage will not be moved

    """
    if x is not None:
       caput('13XRM:m1.VAL', x)
    #endif
    if y is not None:
       caput('13XRM:m2.VAL', y)
    #endif
#enddef


def move_samplestage(position, instrument='IDE_SampleStage', wait=True, timeout=60):
    """
    move SampleStage to named position

    Parameters:
        position (string):    name of sample stage position
        instrument (string):  name of instrument ['IDE_SampleStage']
        wait (True or False): whether to wait for move to complete [True]
        timeout (float):   maximum time in seconds to wait [60.0]

    Example:
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
