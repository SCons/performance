#!/usr/bin/env python2
import os
import sys
import sconstest

def time_make(folder, procs):
    oldwd = os.path.abspath(os.getcwd())
    os.chdir(folder)
    print "%s %s - make" % (procs, folder)
    os.system('%s -o ../results%s/%s/make_cleanbuild.times make -j%s > /dev/null 2>&1' % (sconstest.time, procs, folder, procs))
    os.system('%s -o ../results%s/%s/make_update.times make -j%s > /dev/null 2>&1' % (sconstest.time, procs, folder, procs))
    os.chdir(oldwd)

def time_scons(folder, procs):
    oldwd = os.path.abspath(os.getcwd())
    os.chdir(folder)
    print "%s %s - scons" % (procs, folder)
    os.system('%s -o ../results%s/%s/scons_cleanbuild.times %s %s -j%s > /dev/null 2>&1' % (sconstest.time, procs, folder, sconstest.lscons, sconstest.sconswd, procs))
    os.system('%s -o ../results%s/%s/scons_update.times %s %s -j%s > /dev/null 2>&1' % (sconstest.time, procs, folder, sconstest.lscons, sconstest.sconswd, procs))
    os.system('%s -o ../results%s/%s/scons_update_implicit.times %s %s -j%s --max-drift=1 --implicit-deps-unchanged > /dev/null 2>&1' % (sconstest.time, procs, folder, sconstest.lscons, sconstest.sconswd, procs))
    os.chdir(oldwd)

timelist = ['small',
            'middle',
            'large',
            'vlarge',
            'vvlarge'
           ]

def prepare():
    if 'small' in timelist:
        os.system('python gen-bench.py small 50 100 15 5')
    if 'middle' in timelist:
        os.system('python gen-bench.py middle 100 100 15 5')
    if 'large' in timelist:
        os.system('python gen-bench.py large 200 100 15 5')
    if 'vlarge' in timelist:
        os.system('python gen-bench.py vlarge 300 100 15 5')
    if 'vvlarge' in timelist:
        os.system('python gen-bench.py vvlarge 400 100 15 5')

def main():
    # Run make
    prepare()
    # Default number of processes
    procs = "3"
    if len(sys.argv) > 1:
        procs = sys.argv[1]
    for t in timelist:
        if not os.path.isdir(os.path.join('results%s' % procs, t)):
            os.makedirs(os.path.join('results%s' % procs, t))
#        time_make(t, procs)
#        os.system('rm -rf %s' % t)
    # Run SCons
#    prepare()
    for t in timelist:
        time_scons(t, procs)
        os.system('rm -rf %s' % t)

if __name__ == "__main__":
    main()

