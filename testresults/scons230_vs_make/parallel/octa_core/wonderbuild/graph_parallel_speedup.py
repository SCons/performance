import os
import sys
import glob
import sconstest.eval

def usage():
    print "graph_parallel_speedup.py <scons|make|both> project <build|update> [realtimes]"

prefixes = {'scons' : 'scons_cleanbuild',
            'make' : 'make_cleanbuild'}

def timefile(idx, project, build):
    """ Helper function, constructing the path to the current time result file. """
    return os.path.join('results%d' % idx, project, prefixes[build] + '.times')

def store_times(xdata, ydata, x, r, yfirst, rtimes):
    """ Helper function that stores the times. """
    xdata.append(x)
    if rtimes:
        ydata.append(r)
    else:
        if ydata:
            ydata.append(float(yfirst)/float(r))
        else:
            ydata.append(1.0)
            yfirst = r
    return yfirst

def main():
    if len(sys.argv) < 4:
        usage()
        sys.exit(0)

    rtimes = False
    if len(sys.argv) > 4 and sys.argv[4] == "realtimes":
        rtimes = True

    project = sys.argv[2]
    builds = sys.argv[1]
    both = False
    if builds == "both":
        builds = ['make', 'scons']
        both = True
    else:
        builds = [builds]

    if sys.argv[3] == "update":
        prefixes['scons'] = 'scons_update_implicit'
        prefixes['make'] = 'make_update'

    # Loop over all result folders
    flist = glob.glob('results*')
    xdata = []
    ydata = []
    if both:
        ca = sconstest.eval.DataCurve()
        ca.info.color = 'red'
        ca.info.title = 'make'

        cb = sconstest.eval.DataCurve()
        cb.info.color = 'green'
        cb.info.title = 'scons'
    
    yfirst = 0.0
    y2first = 0.0
    for i in range(len(flist)):
        if both:
            # Pick project for 'make'
            r, u, s = sconstest.eval.getTimeData(timefile(i+1, project, builds[0]))
            if r != 0.0:
                yfirst = store_times(ca.xdata, ca.ydata, i+1, r, yfirst, rtimes)
            else:
                print "Is zero for %d (make)!" % (i+1)

            # Pick project for 'scons'
            r, u, s = sconstest.eval.getTimeData(timefile(i+1, project, builds[1]))
            if r != 0.0:
                y2first = store_times(cb.xdata, cb.ydata, i+1, r, y2first, rtimes)
            else:
                print "Is zero for %d! (scons)" % (i+1)
        else:
            # Pick project
            r, u, s = sconstest.eval.getTimeData(timefile(i+1, project, builds[0]))
        
            if r != 0.0:
                yfirst = store_times(xdata, ydata, i+1, r, yfirst, rtimes)
            else:
                print "Is zero for %d!" % (i+1)

    ytitle = 'Time [s]'
    if not rtimes:
        ytitle = 'Speedup'
    if both:
        if not os.path.isdir('speedup'):
            os.makedirs('speedup')
        sconstest.eval.plotDataCurves([ca, cb], 'speedup/speedup_%s_%s.png' % (project, sys.argv[3]), 'Parallel speedup', 'Cores', ytitle, True)
    else:
        sconstest.eval.plotData(xdata, ydata, 'parallel_speedup_%s.png' % project, 'Parallel speedup', 'Cores', ytitle)

if __name__ == "__main__":
    main()

