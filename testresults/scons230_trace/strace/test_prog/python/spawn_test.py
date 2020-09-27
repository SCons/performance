# Inspired by Trevor Highland (http://blog.melski.net/2013/12/11/update-scons-is-still-really-slow/),
# this little program spawns single processes in quick succession. By allocating more and more memory
# at the same time, the runtimes for the single process calls seems to grow.

import os
import sys

perc='%'

def main():
    cycles = 25000
    append = True
    if len(sys.argv) > 1:
        cycles = int(sys.argv[1])
    if len(sys.argv) > 2:
        append = False

    print "Starting %d cycles..." % cycles
    m_list = []
    cnt = 0
    for i in xrange(cycles):
        cnt += 1
        args = ['echo', '%d/%d (%.2f%s)' % (cnt, cycles, float(cnt)*100.0/float(cycles), perc)]
        os.spawnvpe(os.P_WAIT, args[0], args, os.environ)
        signature ='A'*20000
        if append:
            m_list.append(signature)

    print "Done."

if __name__ == "__main__":
    main()

