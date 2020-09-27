import os
import sys
import shutil
import glob
import sconstest

rnum = "1"
spec = "default"
fast = False
if len(sys.argv) > 1:
  rnum = sys.argv[1]
if len(sys.argv) > 2:
  spec = sys.argv[2]

os.system('python %s%s' % (os.path.join(sconstest.suite, 'prepare.py'),
                           sconstest.redirect))

print "Memwatch run", rnum

# Process all folders
for key, value in sconstest.packages.iteritems():
  print "  %s" % key
  os.system("cd %s; python %s %s" % (value['path'], 
                                     os.path.join(sconstest.suite,"memwatch_single.py"),
                                     key))
  tfiles = glob.glob('%s/*.csv' % value['path'])
  # Ensure that the result folder exists
  if not os.path.isdir(os.path.join(sconstest.results,spec,key)):
    os.makedirs(os.path.join(sconstest.results,spec,key))
  for f in tfiles:
    head, tail = os.path.split(f)
    stem, ext = os.path.splitext(tail)
    shutil.copy(f, os.path.join(sconstest.results,spec,key,stem+rnum+ext))
