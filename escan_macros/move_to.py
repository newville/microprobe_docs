def move_to_map():
   "move to 7.5 keV for mapping"
   open_shutter()
   set_i0amp_gain(50, 'nA/V')
   set_filter(thickness=0)
   detector_distance(90, wait=False)
   move_to_edge('Fe', 'K')
   move_energy(7500)
   fast_mono_tilt()
   autoset_i0amp_gain(take_offsets=False)
   collect_offsets()

def move_to_ce():
   "move to Ce L3 edge"
   open_shutter()
   set_i0amp_gain(50, 'nA/V')
   set_filter(thickness=0)
   detector_distance(90, wait=False)
   move_to_edge('Ce', 'L3')
   autoset_i0amp_gain(take_offsets=False)
   collect_offsets()

def move_to_9keV():
   "move to 9 keV for mapping"
   open_shutter()
   set_i0amp_gain(20, 'nA/V')
   set_filter(thickness=0)
   detector_distance(90, wait=False)
   move_to_edge('Cu', 'K')
   move_energy(9000)
   autoset_i0amp_gain(take_offsets=False)
   collect_offsets()

def filter0():
   set_filter(0)
   autoset_i0amp_gain(take_offsets=False)

def filter50():
   set_filter(50)
   autoset_i0amp_gain(take_offsets=False)

def filter100():
   set_filter(100)
   autoset_i0amp_gain(take_offsets=False)

def filter150():
   set_filter(150)
   autoset_i0amp_gain(take_offsets=False)

def filter200():
   set_filter(200)
   autoset_i0amp_gain(take_offsets=False)

def filter250():
   set_filter(250)
   autoset_i0amp_gain(take_offsets=False)

def filter300():
   set_filter(300)
   autoset_i0amp_gain(take_offsets=False)

def filter350():
   set_filter(350)
   autoset_i0amp_gain(take_offsets=False)
