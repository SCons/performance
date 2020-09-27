#!/usr/bin/env python2
import os
import sys
import sconstest

def time_make(folder):
    oldwd = os.path.abspath(os.getcwd())
    os.chdir(os.path.join(folder, 'make'))
    print "%s - make" % folder
    os.system('%s -o ../../results/%s/make_cleanbuild.times make > /dev/null 2>&1' % (sconstest.time, folder))
    os.system('%s -o ../../results/%s/make_update.times make > /dev/null 2>&1' % (sconstest.time, folder))
    os.chdir(oldwd)

def time_scons(folder):
    oldwd = os.path.abspath(os.getcwd())
    os.chdir(os.path.join(folder, 'scons'))
    print "%s - scons" % folder
    os.system('%s -o ../../results/%s/scons_cleanbuild.times lscons %s > /dev/null 2>&1' % (sconstest.time, folder, sconstest.sconswd))
    os.system('%s -o ../../results/%s/scons_update.times lscons %s > /dev/null 2>&1' % (sconstest.time, folder, sconstest.sconswd))
    os.system('%s -o ../../results/%s/scons_update_implicit.times lscons %s --max-drift=1 --implicit-deps-unchanged > /dev/null 2>&1' % (sconstest.time, folder, sconstest.sconswd))
    os.chdir(oldwd)

timelist = ['small',
            'middle',
            'large',
            'vlarge',
            'vlarge50',
            'vlarge40',
            'vlarge30',
            'vlarge20'
           ]

def prepare():
    if 'small' in timelist:
        os.system('python generate_libs.py small 50 100 15 5')
    if 'middle' in timelist:
        os.system('python generate_libs.py middle 100 100 15 5')
    if 'large' in timelist:
        os.system('python generate_libs.py large 125 100 15 5')
    if 'vlarge' in timelist:
        os.system('python generate_libs.py vlarge 150 100 15 5')
    if 'vlarge20' in timelist:
        os.system('python generate_libs.py vlarge20 200 100 15 5')
    if 'vlarge30' in timelist:
        os.system('python generate_libs.py vlarge30 300 100 15 5')
    if 'vlarge40' in timelist:
        os.system('python generate_libs.py vlarge40 400 100 15 5')
    if 'vlarge50' in timelist:
        os.system('python generate_libs.py vlarge50 500 100 15 5')

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

