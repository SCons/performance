import os
import sys
import sconstest
import sconstest.eval

def usage():
    print "compare_runs.py previous_folder current_folder"

def main():
    if len(sys.argv) < 3:
        usage()
        sys.exit(0)
        
    # Assume that we are comparing two folders
    previous = sys.argv[1]
    current = sys.argv[2]
    resultwd = os.path.join(sconstest.suite, sconstest.results)
    html = os.path.join(resultwd, current, 'comparison.html')
    
    sconstest.eval.compare_folders(resultwd, previous, current, html)

if __name__ == "__main__":
    main()

