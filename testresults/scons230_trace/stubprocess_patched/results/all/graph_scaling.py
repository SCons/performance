import os
import sys
import sconstest.eval

def usage():
    print "graph_scaling.py <scons|make|both> <cleanbuild|update>"

prefixes = {'scons' : 'scons_cleanbuild',
            'make' : 'make_cleanbuild'}

ford = [
        'small', 'middle', 'large', 'vlarge',
        'vlarge20', 'vlarge30', 'vlarge40', 'vlarge50'
       ]

files = {
         'small' : 5000,
         'middle' :10000,
         'large' : 12500,
         'vlarge' : 15000,
         'vlarge20' : 20000,
         'vlarge30' : 30000,
         'vlarge40' : 40000,
         'vlarge50' : 50000
        }

def timefile(project, build):
    return os.path.join('..', project, prefixes[build] + '.times')

def main():
    if len(sys.argv) < 3:
        usage()
        sys.exit(0)

    builds = sys.argv[1]
    both = False
    if builds == "both":
        builds = ['make', 'scons']
        both = True
    else:
        builds = [builds]

    project = sys.argv[2]

    ptitle = "Clean build"
    if project.startswith("upd"):
        prefixes['scons'] = 'scons_update_implicit'
        prefixes['make'] = 'make_update'
        ptitle = "Update"

    # Loop over all result folders
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
            r, u, s = sconstest.eval.getTimeData(timefile(ford[i], builds[0]))
            if r != 0.0:
                ca.xdata.append(files[ford[i]])
                ca.ydata.append(r)
            else:
                print "Is zero for %d (make)!" % (i+1)

            # Pick project for 'scons'
            r, u, s = sconstest.eval.getTimeData(timefile(ford[i], builds[1]))
            if r != 0.0:
                cb.xdata.append(files[ford[i]])
                cb.ydata.append(r)
            else:
                print "Is zero for %d! (scons)" % (i+1)
        else:
            # Pick project
            r, u, s = sconstest.eval.getTimeData(timefile(ford[i], builds[0]))
        
            if r != 0.0:
                # Store time
                xdata.append(files[ford[i]])
                ydata.append(r)
            else:
                print "Is zero for %d!" % (i+1)

    ytitle = 'Time [s]'
    if both:
        sconstest.eval.plotDataCurves([ca, cb], '%s.png' % project, ptitle, 'CPP files', 
                                      ytitle, True, yzero=True)
    else:
        sconstest.eval.plotData(xdata, ydata, '%s_%s.png' % (builds[0], project), ptitle, 'CPP files', ytitle)


if __name__ == "__main__":
    main()

