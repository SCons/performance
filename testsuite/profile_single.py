import os
import sys
import sconstest

optargs=''
fast = False
if len(sys.argv) > 1:
  optargs=sconstest.packages[sys.argv[1]].get('optargs','')
if len(sys.argv) > 2 and sys.argv[2] == 'fast':
  fast = True

os.system("%s prof.results %s%s%s" % (sconstest.lsconsprof, sconstest.sconswd, optargs, sconstest.redirect))
os.system("%s prof_update.results %s%s%s" % (sconstest.lsconsprof, sconstest.sconswd, optargs, sconstest.redirect))
if not fast:
  os.system("%s prof_update_implicit.results %s --max-drift=1 --implicit-deps-unchanged%s%s" % (sconstest.lsconsprof, sconstest.sconswd, optargs, sconstest.redirect))

