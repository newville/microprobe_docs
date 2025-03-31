def move_to_12kev():
   "move to As K edge"
   open_shutter()
   set_i0amp_gain(100, 'nA/V')
   set_i1amp_gain(500, 'nA/V')
   move_to_edge('As', 'K')
   detector_distance(120)
   move_energy(12000)
   autoset_i0amp_gain(take_offsets=False)
   collect_offsets()

def move_to_as():
   "move to As K edge"
   open_shutter()
   set_i0amp_gain(100, 'nA/V')
   set_i1amp_gain(500, 'nA/V')
   detector_distance(120)
   move_to_edge('As', 'K')
   autoset_i0amp_gain(take_offsets=False)
   collect_offsets()


def move_to_19kev():
   "move to Zr K edge"
   open_shutter()
   set_i0amp_gain(20, 'nA/V')
   set_i1amp_gain(500, 'nA/V')
   move_to_edge('Zr', 'K')
   move_energy(19000)
   detector_distance(120)
   set_filter(thickness=200)
   autoset_i0amp_gain(take_offsets=False)
   collect_offsets()


def move_to_cu():
   "move to Cu K edge"
   open_shutter()
   set_i0amp_gain(100, 'nA/V')
   set_i1amp_gain(500, 'nA/V')
   move_to_edge('Cu', 'K')
   autoset_i0amp_gain(take_offsets=False)
   collect_offsets()

def move_to_fe():
   "move to Fe K edge"
   open_shutter()
   set_i0amp_gain(100, 'nA/V')
   set_i1amp_gain(500, 'nA/V')
   set_filter(thickness=300)
   detector_distance(120)
   move_to_edge('Fe', 'K')
   autoset_i0amp_gain(take_offsets=False)
   collect_offsets()

def move_to_mn():
   "move to Mn K edge"
   open_shutter()
   set_i0amp_gain(500, 'nA/V')
   set_i1amp_gain(500, 'nA/V')
   set_filter(thickness=0)
   move_to_edge('Mn', 'K')
   detector_distance(75)
   autoset_i0amp_gain(take_offsets=False)
   collect_offsets()

def move_to_ti():
   "move to Ti K edge"
   open_shutter()
   set_filter(thickness=0)
   set_i0amp_gain(200, 'nA/V')
   set_i1amp_gain(10, 'nA/V')
   move_to_edge('Ti', 'K')
   autoset_i0amp_gain(take_offsets=False)
   collect_offsets()

def move_to_eu():
   "move to Eu L3 edge"
   open_shutter()
   set_filter(thickness=100)
   set_i0amp_gain(100, 'nA/V')
   set_i1amp_gain(20, 'nA/V')
   move_to_edge('Eu', 'L3')
   autoset_i0amp_gain(take_offsets=False)
   collect_offsets()

def move_to_au():
   "move to Au L3 edge"
   open_shutter()
   set_i0amp_gain(50, 'nA/V')
   set_i1amp_gain(200, 'nA/V')
   move_to_edge('Au', 'L3')
   autoset_i0amp_gain(take_offsets=False)
   collect_offsets()
