#!/usr/bin/env python2
import os
import sys
import sconstest

def time_make(folder):
    oldwd = os.path.abspath(os.getcwd())
    os.chdir(folder)
    print "%s - make" % folder
    os.system('%s -o ../results/%s/make_cleanbuild.times make > /dev/null 2>&1' % (sconstest.time, folder))
    os.system('%s -o ../results/%s/make_update.times make > /dev/null 2>&1' % (sconstest.time, folder))
    os.chdir(oldwd)

def time_scons(folder):
    oldwd = os.path.abspath(os.getcwd())
    os.chdir(folder)
    print "%s - scons" % folder
    os.system('%s -o ../results/%s/scons_cleanbuild.times lscons %s > /dev/null 2>&1' % (sconstest.time, folder, sconstest.sconswd))
    os.system('%s -o ../results/%s/scons_update.times lscons %s > /dev/null 2>&1' % (sconstest.time, folder, sconstest.sconswd))
    os.system('%s -o ../results/%s/scons_update_implicit.times lscons %s --max-drift=1 --implicit-deps-unchanged > /dev/null 2>&1' % (sconstest.time, folder, sconstest.sconswd))
    os.chdir(oldwd)

timelist = ['small',
            'middle',
            'large',
            'vlarge'
           ]

def prepare():
    if 'small' in timelist:
        os.system('python gen-bench.py small 50 100 15 5')
    if 'middle' in timelist:
        os.system('python gen-bench.py middle 100 100 15 5')
    if 'large' in timelist:
        os.system('python gen-bench.py large 125 100 15 5')
    if 'vlarge' in timelist:
        os.system('python gen-bench.py vlarge 150 100 15 5')

def main():
    # Run make
    prepare()
    for t in timelist:
        if not os.path.isdir(os.path.join('results', t)):
            os.makedirs(os.path.join('results', t))
        time_make(t)
        os.system('rm -rf %s' % t)
    # Run SCons
    prepare()
    for t in timelist:
        time_scons(t)
        os.system('rm -rf %s' % t)

if __name__ == "__main__":
    main()

