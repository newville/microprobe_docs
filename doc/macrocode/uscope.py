##
## code to support Off-line Microscope and
## transfer of coordinates to Sample Stage
##
## main functions:
##
## .... uscope2sample(suffix='') ....
##
## transfer all named positions saved for the IDE Microscope (off-line)
## to IDE SampleStage (on-line), applying the rotation matrix saved by
## the function `make_uscope_rotation()`
##
##
## .... make_uscope_rotation() ....
##
## calculate and store best rotation matrix to transform positions from
## the IDE Microscope (off-line) to IDE SampleStage (on-line).
##
## this uses position names that are the same in both instruments, and
## requires at least 6 such positions. That is, save positions with the
## same names in both the IDE_Microscope and IDE_SampleStage.
## Positions names not found in both instruments are ignored.
##########################################################################
##

import json
from collections import OrderedDict

# if not hasattr(_scan, '_instdb'):
#     connect_scandb(dbname='epics_scan',
#                 server='postgresql',
#                 host='ion.cars.aps.anl.gov',
#                 user='epics',
#                 password='microXAFS@13IDE')
# #endif


def read_uscope_xyz(name = 'IDE_Microscope'):
    """read XYZ Positions from IDE Microscope Instrument
    returns dictionary of PositionName: (x, y, z)
    """
    out = OrderedDict()
    instdb = _scan._instdb
    for pname in instdb.get_positionlist(name):
        thispos = instdb.get_position(name, pname)
        vals = [float(p.value) for p in thispos.pvs]
        out[pname] = vals
    #endfor
    return out
#enddef

def read_sample_xyz(name = 'IDE_SampleStage'):
    """read XYZ Positions from IDE SampleStage Instrument
    returns dictionary of PositionName: (x, y, z)

    Note: FineX, FineY and Theta stages are not included
    """
    out = OrderedDict()
    instdb = _scan._instdb
    for pname in instdb.get_positionlist(name):
        thispos = instdb.get_position(name, pname)
        vals = [float(p.value) for p in thispos.pvs]
        vals = [vals[3], vals[5], vals[4]]
        out[pname] = vals
    #endfor
    return out
#enddef


def params2rotmatrix(params, mat):
    """--private--  turn fitting parameters
    into rotation matrix
    """
    mat[0][1] = params.c01
    mat[1][0] = params.c10
    mat[0][2] = params.c02
    mat[2][0] = params.c20
    mat[1][2] = params.c12
    mat[2][1] = params.c21
    return mat
#enddef

def resid_rotmatrix(params, mat, v1, v2):
    "--private-- resdiual function for fit"
    mat = params2rotmatrix(params, mat)
    return (v2 - dot(mat, v1)).flatten()
#enddef


def calc_rotmatrix(d1, d2):
    """get best-fit rotation matrix to transform coordinates
    from 1st position dict into the 2nd position dict
    """
    labels = []
    d2keys = d2.keys()
    for x in d1.keys():
        if x in d2keys:
            labels.append(x)
        #endif
    #endfor
    labels.sort()
    if len(labels) < 6:
        print """Error: need at least 6 saved positions
  in common to calculate rotation matrix"""

        return None, None, None
    #endif
    v1 = ones((4, len(labels)))
    v2 = ones((4, len(labels)))
    for i, label in enumerate(labels):
        v1[0, i] = d1[label][0]
        v1[1, i] = d1[label][1]
        v1[2, i] = d1[label][2]
        v2[0, i] = d2[label][0]
        v2[1, i] = d2[label][1]
        v2[2, i] = d2[label][2]
    #endfor

    # get initial rotation matrix, assuming that
    # there are orthogonal coordinate systems.
    mat = transforms.superimposition_matrix(v1, v2, scale=True)

    params = group(c10   = param(mat[1][0], vary=True),
                   c01   = param(mat[0][1], vary=True),
                   c20   = param(mat[2][0], vary=True),
                   c02   = param(mat[0][2], vary=True),
                   c12   = param(mat[1][2], vary=True),
                   c21   = param(mat[2][1], vary=True) )

    fit_result = minimize(resid_rotmatrix, params, args=(mat, v1, v2))
    mat = params2rotmatrix(params, mat)
    return mat, v1, v2
#enddef


##
## Main Interface
##

def make_uscope_rotation():
    """Calculate the rotation maxtrix needed to convert
    IDE Microscope (off-line) to IDE SampleStage (on-line)

    This calculates the rotation matrix based on all
    positions names that occur in the Position List for
    both instruments.

    The result is saved as a json dictionary of the
    IDE_Microscope instrument

    No arguments.
    """

    d1 = read_uscope_xyz()
    d2 = read_sample_xyz()
    # calculate the rotation matrix
    mat, v1, v2 = calc_rotmatrix(d1, d2)
    if mat is None:
        return
    #endif

    # now save to 'notes' for the Microscope instrument
    uscope = _scan._instdb.get_instrument('IDE_Microscope')
    notes = uscope.notes
    if notes is None:
        notes = {}
    else:
        notes = json.loads(notes)
    #endif
    notes['rotmat2SampleStage'] = mat.tolist()
    uscope.notes = json.dumps(notes)
    _scan._scandb.commit()
    return mat
#enddef

def uscope2sample(suffix=''):
    """transfer all named positions saved for the
    IDE Microscope (off-line) to IDE SampleStage (on-line)

    Applies the rotation matrix saved by the function

      `make_uscope_rotation()`

    Arguments
    ---------
     suffix: string, default ''
        suffix to apply when transferring names, so as
        to avoid name clashes -- otherwise previously
        saved positions named may be overwritten.

    """
    uscope = _scan._instdb.get_instrument('IDE_Microscope')
    sample = _scan._instdb.get_instrument('IDE_SampleStage')
    try:
        notes = json.loads(uscope.notes)
        rotmat = array(notes['rotmat2SampleStage'])
    except:
        print(" Error:  could not get rotation matrix!")
        return
    #endtry
    upos   = read_uscope_xyz()
    labels = upos.keys()

    v = ones((4, len(labels)))
    for i, key in enumerate(labels):
        v[0, i] = upos[key][0]
        v[1, i] = upos[key][1]
        v[2, i] = upos[key][2]
    #endfor

    # Predict coordinates in SampleStage coordination system
    pred = dot(rotmat, v)

    # make SampleStage coordinates
    stage = _scan._instdb.get_instrument('IDE_SampleStage')
    spos = OrderedDict()
    for pv in stage.pvs:
        spos[pv.name] = 0.000
    #endfor
    xpv, ypv, zpv = '13XRM:m4.VAL', '13XRM:m6.VAL', '13XRM:m5.VAL'
    for i, label in enumerate(labels):
        spos[xpv] = pred[0, i]
        spos[ypv] = pred[1, i]
        spos[zpv] = pred[2, i]
        nlabel = '%s%s' % (label, suffix)
        _scan._instdb.save_position('IDE_SampleStage', nlabel, spos)
    #endfor
#enddef
