import os
import sys
import glob
import sconstest.eval

def usage():
    print "graph_scaling.py <scons|make|both> results_idx <build|update>"

prefixes = {'scons' : 'scons_cleanbuild',
            'make' : 'make_cleanbuild'}

ford = ['small', 'middle', 'large', 'vlarge', 'vvlarge']

files = {'small' : 5000,
         'middle' : 10000,
         'large' : 20000,
         'vlarge' : 30000,
         'vvlarge' : 40000}

def timefile(idx, project, build):
    """ Helper function, constructing the path to the current time result file. """
    return os.path.join('results%s' % idx, project, prefixes[build] + '.times')

def main():
    if len(sys.argv) < 4:
        usage()
        sys.exit(0)

    project = sys.argv[2]
    builds = sys.argv[1]
    both = False
    if builds == "both":
        builds = ['make', 'scons']
        both = True
    else:
        builds = [builds]

    ptitle = "Clean build"
    if sys.argv[3] == "update":
        prefixes['scons'] = 'scons_update_implicit'
        prefixes['make'] = 'make_update'
        ptitle = "Update"

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

    for i in range(len(ford)):
        if both:
            # Pick project for 'make'
            r, u, s = sconstest.eval.getTimeData(timefile(sys.argv[2], ford[i], builds[0]))
            if r != 0.0:
                ca.xdata.append(files[ford[i]])
                ca.ydata.append(r)
            else:
                print "Is zero for %d (make)!" % (i+1)
 
            # Pick project for 'scons'
            r, u, s = sconstest.eval.getTimeData(timefile(sys.argv[2], ford[i], builds[1]))
            if r != 0.0:
                cb.xdata.append(files[ford[i]])
                cb.ydata.append(r)
            else:
                print "Is zero for %d (scons)!" % (i+1)
        else:
            # Pick project
            r, u, s = sconstest.eval.getTimeData(timefile(sys.argv[2], ford[i], sys.argv[1]))
        
            if r != 0.0:
                # Store time
                xdata.append(files[ford[i]])
                ydata.append(r)
            else:
                print "Is zero for %d!" % (i+1)

    if both:
        if not os.path.isdir('scaling'):
            os.makedirs('scaling')
        sconstest.eval.plotDataCurves([ca, cb], 'scaling/scaling_%s_%s.png' % (project, sys.argv[3]), ptitle, 'CPP files', legend=True)
    else:
        sconstest.eval.plotData(xdata, ydata, 'scaling_%s.png' % project, 'Linear scaling', 'CPP files')

if __name__ == "__main__":
    main()

