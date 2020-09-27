import os
import sys
import subprocess
import time
import sconstest

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


optargs=''
if len(sys.argv) > 1:
  optargs=sconstest.packages[sys.argv[1]].get('optargs','')

# Start mem_watch in background
subprocess.Popen(["python",os.path.join(sconstest.suite,"mem_watch.py"),"mem.csv"])
time.sleep(1)
# Start scons in foreground
os.system("%s %s%s%s" % (sconstest.lscons, sconstest.sconswd, optargs, sconstest.redirect))
time.sleep(2)
# Wait for memwatch to finish
while getMemwatchPID():
    time.sleep(1)

# Start mem_watch in background
subprocess.Popen(["python",os.path.join(sconstest.suite, "mem_watch.py"),"mem_update.csv"])
time.sleep(1)
# Start scons in foreground
os.system("%s %s%s%s" % (sconstest.lscons, sconstest.sconswd, optargs, sconstest.redirect))
time.sleep(2)
# Wait for memwatch to finish
while getMemwatchPID():
    time.sleep(1)

