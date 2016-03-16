import sys
import os
import shutil

src  = '//cars5/Data/xas_user/scan_config/13ide/macros'
dest = 'doc/macros'

for fname in os.listdir(src):
    if fname.endswith('.lar'):
        pname = '%s.py' % fname[:-4]
        fsrc = os.path.join(src, fname)
        fdst = os.path.join(dest, pname)
        print fsrc, fdst
        shutil.copy(fsrc, fdst)
