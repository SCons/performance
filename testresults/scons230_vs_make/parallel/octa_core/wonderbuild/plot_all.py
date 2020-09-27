import os
import sys
import glob

ford = ['small', 'middle', 'large', 'vlarge', 'vvlarge']

def main():
    os.system("rm -rf scaling")
    os.system("rm -rf speedup")

    # Loop over all result folders
    flist = glob.glob('results*')

    print "Linear scaling"
    for i in range(len(flist)):
        print "  ", (i+1)
        os.system("python graph_scaling.py both %d build" % (i+1))
        os.system("python graph_scaling.py both %d update" % (i+1))

    print "Parallel speedup"
    for f in ford:
        print "  ", f
        os.system("python graph_parallel_speedup.py both %s build" % f)

if __name__ == "__main__":
    main()

