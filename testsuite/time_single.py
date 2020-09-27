import os
import sys
import sconstest

optargs=''
fast = False
if len(sys.argv) > 1:
  optargs=sconstest.packages[sys.argv[1]].get('optargs','')
if len(sys.argv) > 2 and sys.argv[2] == 'fast':
  fast = True

os.system("%s -o run.times %s %s%s%s" % (sconstest.time, sconstest.lscons, sconstest.sconswd, optargs, sconstest.redirect))
os.system("%s -o update.times %s %s%s%s" % (sconstest.time, sconstest.lscons, sconstest.sconswd, optargs, sconstest.redirect))
if not fast:
  os.system("%s -o update_implicit.times %s %s --max-drift=1 --implicit-deps-unchanged%s%s" % (sconstest.time, sconstest.lscons, sconstest.sconswd, optargs, sconstest.redirect))
