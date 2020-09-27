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

def getPIDFromLine(line):
    return line.split()[1]
    
def getSConsPID():
    for p in getProcesses():
        if 'python' in p and sconstest.sconswd in p:
            return getPIDFromLine(p)

    return '0'    

def pidIsStillAlive(pid):
    for p in getProcesses():
        if pid in getPIDFromLine(p):
            return True
    
    return False

def getCurrentMem(pid):
    status = stdoutCmd(['cat','/proc/%s/status' % pid])
    if not status:
        return None

    for s in status.splitlines():
        if 'VmSize:' in s:
            slist = s.split()
            if len(slist) == 3:
                return slist[1]
    return '0'

# Set to True for additional debug output
debug = False

def main():
    pid = getSConsPID()

    while pid == '0':
        if debug:
            print "Waiting for SCons..."
        time.sleep(1.0)
        pid = getSConsPID()

    if debug:
        print "Watching PID %s" % pid

    fname = 'mem.csv'
    if len(sys.argv) > 1:
        fname = sys.argv[1]


    fout = open(fname, 'w')

    i = 0
    mx = 0
    m = getCurrentMem(pid)
    if m and int(m) > mx:
        mx = int(m)
    while pidIsStillAlive(pid):
        fout.write("%d,%s\n" % (i,m))
        if debug:
            print "%s" % m
        i += 1
        time.sleep(1.0)
        m = getCurrentMem(pid)
        if m and int(m) > mx:
            mx = int(m)

    fout.close()
    print "Max: ", mx

if __name__ == "__main__":
    main()

