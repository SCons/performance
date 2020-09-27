import os
import sys
import sconstest.eval

def main():
    ptitle = "Accumulated time"

    xdata = []
    ydata = []

    ca = sconstest.eval.DataCurve()
    ca.info.color = 'green'
    ca.info.title = 'first'
    ca.info.marker = ''

    cb = sconstest.eval.DataCurve()
    cb.info.color = 'red'
    cb.info.title = 'second'
    cb.info.marker = ''
 
    with open('first.csv','r') as afile:
        acsv = afile.readlines()
    with open('second.csv','r') as bfile:
        bcsv = bfile.readlines()

    smaller = min(len(acsv), len(bcsv))
    acsv = acsv[:smaller]
    bcsv = bcsv[:smaller]

    for aline, bline in zip(acsv, bcsv):
        al = aline.rstrip('\n').split(',')
        ca.xdata.append(int(al[0].strip()))
        ca.ydata.append(float(al[1].strip()))
        
        bl = bline.rstrip('\n').split(',')
        cb.xdata.append(int(bl[0].strip()))
        cb.ydata.append(float(bl[1].strip()))

    ytitle = 'Time [s]'
    sconstest.eval.plotDataCurves([ca, cb], 'times.png', ptitle, 'SysCall', 
                                      ytitle, True, yzero=True)

if __name__ == "__main__":
    main()

