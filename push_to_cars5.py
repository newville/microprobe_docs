import sys
import os
import shutil

dest = '/cars5/Data/xas_user/scan_config/13ide/macros'
dest = 'larch_macros'
src = 'doc/macros'

for fname in os.listdir(src):
    if fname.endswith('.py') and not fname.startswith('__'):
        dname = '%s.lar' % fname[:-3]
        fsrc = os.path.join(src,  fname)
        fdst = os.path.join(dest, dname)
        print fsrc, fdst
        shutil.copy(fsrc, fdst)
