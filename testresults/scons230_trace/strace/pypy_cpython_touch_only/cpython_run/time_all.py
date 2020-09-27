#!/usr/bin/env python2
import os
import sys
import sconstest
import time
import subprocess

def stdoutCmd(args):
    process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sout, serr = process.communicate()

    return sout

def getProcesses():
    return stdoutCmd(['ps','-ef']).splitlines()

def getMemwatchPID():
    pid = None
    for p in getProcesses():
        if 'python' in p and 'mem_watch' in p:
            pid = p.split()[1]

    return pid

def time_make(folder):
    oldwd = os.path.abspath(os.getcwd())
    os.chdir(folder)
    print "%s - writing project files" % folder
    os.system('./genscons.pl > /dev/null 2>&1')
    os.chdir('sconsbld')
    print "%s - make" % folder
    os.system('%s -o ../../results/%s/make_cleanbuild.times make > /dev/null 2>&1' % (sconstest.time, folder))
    print "%s - make update" % folder
    os.system('%s -o ../../results/%s/make_update.times make > /dev/null 2>&1' % (sconstest.time, folder))
    os.chdir(oldwd)

def time_scons(folder):
    oldwd = os.path.abspath(os.getcwd())
    os.chdir(folder)
    print "%s - writing project files" % folder
    os.system('./genscons.pl > /dev/null 2>&1')
    os.chdir('sconsbld')

    print "%s - scons" % folder
    # Start mem_watch in background
    subprocess.Popen(["python",os.path.join(sconstest.suite,"mem_watch.py"),"../../results/%s/mem.csv" % folder])
    time.sleep(1)
    os.system('%s -o ../../results/%s/scons_cleanbuild.times lscons %s > /dev/null 2>&1' % (sconstest.time, folder, sconstest.sconswd))
    time.sleep(2)
    # Wait for memwatch to finish
    while getMemwatchPID():
        time.sleep(1)

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
    # Run make
    for t in timelist:
        if not os.path.isdir(os.path.join('results', t)):
            os.makedirs(os.path.join('results', t))
        time_scons(t)
        os.system('rm -rf %s/sconsbld' % t)

if __name__ == "__main__":
    main()

