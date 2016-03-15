def restart_server():
   """
   shutdown, restart scan server.
   WARNING : only do this if you are sure of what you're doing!
   Consult Matt and Tony before using
   """
   caput('13XRM:SCANDB:Shutdown', 1)
#enddef


def check_scan_abort():
    "returns whether Abort has been requested"
    return get_dbinfo('request_abort', as_bool=True)
#enddef

def low_flux():
   """
   Set to 'low flux' conditions
   Note that details vary for each user, and you should
   consult Matt and Tony before using
   """
   caput('13IDA:m6.VAL', 0.10)
   caput('13IDA:m8.VAL', 0.20)
   caput('13IDA:m70.VAL', 0.03)
   set_i0amp_gain(2, 'nA/V')
   sleep(10)
   set_mono_tilt()
#enddef

def high_flux():
   """
   Set to 'high flux' conditions.
   Note that details vary for each user, and you should
   consult Matt and Tony before using
   """
   caput('13IDA:m6.VAL', 0.80)
   caput('13IDA:m8.VAL', 0.25)
   caput('13IDA:m70.VAL', 0.08)
   set_i0amp_gain(10, 'nA/V')
   sleep(10)
   set_mono_tilt()
#enddef

def focus2():
   """
   Focus beam to approximately 2 microns.
   Note that details vary for each user, and you should
   consult Matt and Tony before using
   """
   move_instrument('Small KB Forces', 'focus_2um', wait=True)
#enddef

def focus5():
   """
   Focus beam to approximately 10 microns.
   Note that details vary for each user, and you should
   consult Matt and Tony before using
   """
   move_instrument('Small KB Forces', 'focus_5um', wait=True)
#enddef

def focus10():
   """
   Focus beam to approximately 10 microns.
   Note that details vary for each user, and you should
   consult Matt and Tony before using
   """
   move_instrument('Small KB Forces', 'focus_10um', wait=True)
#enddef


