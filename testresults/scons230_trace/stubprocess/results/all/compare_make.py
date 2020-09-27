import os
import sys
import sconstest.eval

prefixes = {'single' : 'scons_cleanbuild',
            'parallel' : 'make_cleanbuild'}

ford = [
        'f', 'g', 'h', 'i',
        'j', 'k', 'l', 'm',
        'n', 'o', 'p'
       ]

files = {
         'f' : 24500,
         'g' : 32500,
         'h' : 40500,
         'i' : 48500,
         'j' : 56500,
         'k' : 64500,
         'l' : 72500,
         'm' : 80500,
         'n' : 88500,
         'o' : 96500,
         'p' : 104500
        }

def timefile(project, build, otherdir='..'):
    return os.path.join(otherdir, project, prefixes[build] + '.times')

def main():
    builds = ['single','parallel']
    both = True

    project = 'clean'

    ptitle = "Clean builds (stubprocess)"

    # Loop over all result folders
    xdata = []
    ydata = []

    if both:
        ca = sconstest.eval.DataCurve()
        ca.info.color = 'green'
        ca.info.title = 'Stubprocess (posix_spawn)'

        cb = sconstest.eval.DataCurve()
        cb.info.color = 'red'
        cb.info.title = 'Make'
 
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
            r, u, s = sconstest.eval.getTimeData(timefile(ford[i], builds[1], 
                                                 os.path.join('..','..','..','..','batchbuild','single_core','results')))
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
        sconstest.eval.plotDataCurves([ca, cb], 'compare_%s_make.png' % project, ptitle, 'C files', 
                                      ytitle, True, yzero=True)
    else:
        sconstest.eval.plotData(xdata, ydata, '%s_%s.png' % (builds[0], project), ptitle, 'C files', ytitle)


if __name__ == "__main__":
    main()

