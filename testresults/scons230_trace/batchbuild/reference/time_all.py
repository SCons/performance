#!/usr/bin/env python2
import os
import sys
import sconstest

def time_scons(folder):
    oldwd = os.path.abspath(os.getcwd())
    os.chdir(folder)
    print "%s - writing project files" % folder
    os.system('./genscons.pl > /dev/null 2>&1')
    os.chdir('sconsbld')

    print "%s - scons" % folder
    # Start mem_watch in background
    os.system('%s -o ../../results/%s/scons_cleanbuild.times lscons %s > /dev/null 2>&1' % (sconstest.time, folder, sconstest.sconswd))

    print "%s - scons update" % folder
    # Start mem_watch in background
    os.system('%s -o ../../results/%s/scons_update.times lscons %s > /dev/null 2>&1' % (sconstest.time, folder, sconstest.sconswd))

    print "%s - scons update cached" % folder
    # Start mem_watch in background
    os.system('%s -o ../../results/%s/scons_update_implicit.times lscons %s --max-drift=1 --implicit-deps-unchanged > /dev/null 2>&1' % (sconstest.time, folder, sconstest.sconswd))
    os.chdir(oldwd)

timelist = ['f',
            'g',
            'h',
            'i',
            'j',
            'k',
            'l',
            'm',
            'n',
            'o',
            'p'
           ]

def main():
    # Run SCons
    for t in timelist:
        if not os.path.isdir(os.path.join('results', t)):
            os.makedirs(os.path.join('results', t))
        time_scons(t)
        os.system('rm -rf %s/sconsbld' % t)

if __name__ == "__main__":
    main()

