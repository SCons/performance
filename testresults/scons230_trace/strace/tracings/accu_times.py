import sys

def usage():
    print "accu_times.py <input.txt>"

def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(0)

    cnt = 0
    acctime = 0.0
    with open(sys.argv[1], "r") as f:
        for l in f:
            sl = l.split()
            if len(sl) > 2:
                try:
                    t = float(sl[1])
                    acctime += t
                    cnt += 1
                    print "%d, %.8f" % (cnt, acctime)
                except:
                    pass

if __name__ == "__main__":
    main()

