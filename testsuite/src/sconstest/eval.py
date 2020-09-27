import os
import sys
import glob
import re
import pstats
import sconstest

has_csv = True
try:
    import csv
except:
    has_csv = False
    
has_matplot = True
try:
    import matplotlib.pyplot as plt
except:
    has_matplot = False

def usage():
    print "Usage: eval"

def plotCsvFile(csvpath, pngpath, csvtitle='', xaxis='secs', yaxis='KByte'):
    """ Plot the given CSV file into a PNG image.
    """
    if has_csv and has_matplot:
        csv_reader = csv.reader(open(csvpath))
        bigx = float(-sys.maxint -1)
        bigy = float(-sys.maxint -1)
        smallx = float(sys.maxint)
        smally = float(sys.maxint)
        
        verts = []
        for row in csv_reader:
            verts.append(row)
            if float(row[0]) > bigx:
                bigx = float(row[0])
            if float(row[1]) > bigy:
                bigy = float(row[1])
            if float(row[0]) < smallx:
                smallx = float(row[0])
            if float(row[1]) < smally:
                smally = float(row[1])
        x_arr = []
        y_arr = []
        for vert in verts:
            x_arr.append(vert[0])
            y_arr.append(vert[1])
        
        plt.clf()
        plt.plot(x_arr, y_arr, color='blue', lw=1)
        plt.xlabel(xaxis)
        plt.ylabel(yaxis)
        plt.title(csvtitle)
        
        plt.savefig(pngpath)

class DataCurveInfo:
    def __init__(self):
        self.color = 'blue'
        self.marker = 'o'
        self.linewidth = 1
        self.linestyle = '-'
        self.title = ''
        
class DataCurve:
    def __init__(self):
        self.xdata = []
        self.ydata = []
        self.info = DataCurveInfo()

def plotData(xdata, ydata, pngpath, ftitle='', 
              xaxis='Files', yaxis='Time [s]',
              yzero=False):
    """ Plot the given X/Y data into a PNG image.
    """
    if has_matplot:
        plt.clf()
        plt.plot(xdata, ydata, color='blue', marker='o', lw=1)
        plt.xlabel(xaxis)
        plt.ylabel(yaxis)
        plt.title(ftitle)
        
        if yzero:
            # Force y axis to show values including
            # (or: starting from) zero...
            x1,x2,y1,y2 = plt.axis()
            if y1 > 0.0:
                plt.axis((x1,x2,0.0,y2))
        plt.savefig(pngpath)

def plotDataCurves(curves, pngpath, ftitle='', 
                     xaxis='Files', yaxis='Time [s]',
                     legend=False, legendloc='upper left',
                     yzero=False):
    """ Plot the given X/Y data into a PNG image.
    """
    if has_matplot:
        plt.clf()
        for c in curves:
            plt.plot(c.xdata, c.ydata, color=c.info.color,
                     marker=c.info.marker, linestyle=c.info.linestyle,
                     lw=c.info.linewidth, label=c.info.title)
        plt.xlabel(xaxis)
        plt.ylabel(yaxis)
        plt.title(ftitle)
        if legend:
            plt.legend(loc=legendloc)
        
        if yzero:
            # Force y axis to show values including
            # (or: starting from) zero...
            x1,x2,y1,y2 = plt.axis()
            if y1 > 0.0:
                plt.axis((x1,x2,0.0,y2))
        plt.savefig(pngpath)

        
def secondsFromTime(tstr):
    """ Return the given time string in seconds.
    """
    tl = tstr.split(':')
    secs = 0.0
    if len(tl) > 1:
        if len(tl) >= 3:
            try:
                secs = float(tl[0])*3600+float(tl[1])*60.0+float(tl[2])
            except:
                pass
            return secs
        else:
            try:
                secs = float(tl[0])*60+float(tl[1])
            except:
                pass
            return secs
    
    try:
        secs = float(tstr)
    except:
        pass
    return secs

def getTimeData(fpath):
    """ Return the single time values (elapsed/user/system)
        from the given *.times file.
    """
    f = open(fpath,"r")
    content = f.read().replace("\n", "")
    f.close()

    ml = content.strip().split(',')
    if len(ml) == 3:
        return (secondsFromTime(ml[0].strip()), 
               secondsFromTime(ml[1].strip()),
               secondsFromTime(ml[2].strip()))

    return (0.0,0.0,0.0)    

def getHighestMemValue(fpath):
    """ Return the highest memory value for the
        given CSV file fpath.
    """
    f = open(fpath,"r")
    maxmem = 0
    for l in f:
        ll = l.rstrip('\n').split(',')
        if len(ll) > 1:
            try:
                curmem = int(ll[1])
                if curmem > maxmem:
                    maxmem = curmem
            except:
                pass
    f.close()

    return maxmem

class TimeInfo:
    """ Stores the single results and median values
        for the single runs (run/update/implicit) of
        a single package.
    """
    def __init__(self, name):
        self.name = name
        self.real = []
        self.user = []
        self.system = []
        self.real_m = 0.0
        self.user_m = 0.0
        self.system_m = 0.0

    def getTimes(self, path, prefix):
        fl = glob.glob(os.path.join(path,prefix)+'?.times')
        cnt = len(fl)
        treal = 0.0
        tusr = 0.0
        tsys = 0.0
        if cnt:
            for f in sorted(fl):
                r, u, s = getTimeData(f)
                treal += float(r)
                tusr += float(u)
                tsys += float(s)
                self.real.append(float(r))
                self.user.append(float(u))
                self.system.append(float(s))
                
            self.real_m = treal/float(cnt)
            self.user_m = tusr/float(cnt)
            self.system_m = tsys/float(cnt)
            return self.real_m, self.user_m, self.system_m
        
        return 0.0,0.0,0.0

    def renderHtml(self, out):
        out.write("<table border=1>\n")
        out.write("<tr><th>Run</th><th>Elapsed [s]</th><th>User [s]</th><th>System [s]</th></tr>\n")
        for idx in range(len(self.real)):
            out.write('<tr><td align="right">%d</td><td align="right">%.1f</td><td align="right">%.1f</td><td align="right">%.1f</td></tr>\n' % (idx+1,
                                         self.real[idx],
                                         self.user[idx],
                                         self.system[idx]))
        out.write('<tr><td align="right">Median</td><td align="right">%.1f</td><td align="right">%.1f</td><td align="right">%.1f</td></tr>\n' % (self.real_m,
                                     self.user_m,
                                     self.system_m))
        out.write("</table>\n")

time_list = ['run', 'update', 'update_implicit']

class PackageTimes:
    """ Stores the run time infos
        for the different prefixes (run/update/implicit)
        of a single package.
    """
    def __init__(self):
        self.times = {}

    def readTimes(self, path):
        # Loop over all known time prefixes
        for p in time_list:
            ti = TimeInfo(p)
            ti.getTimes(path, p)
            self.times[p] = ti

    def renderHtml(self, out):
        # Loop over all known time prefixes
        for key in time_list:
            out.write("<h4>%s</h4>\n" % key)
            self.times[key].renderHtml(out)


    def renderCompareHtml(self, other, out):
        # Loop over all known time_list
        out.write("<table border=1>\n")
        out.write("<tr><th>Run</th>")
        comp = []
        for t in time_list:
            if t in self.times and t in other.times and self.times[t].real_m != 0.0:
                comp.append(t)
        # Header line
        for c in comp:
            out.write("<th>%s [s]</th>" % c)
        out.write("</tr>\n")
        # Previous run
        out.write('<tr><td align="right">Previous</td>')
        for c in comp:
            out.write('<td align="right">%.1f</td>' % self.times[c].real_m)
        out.write("</tr>\n")
        # Current run
        out.write('<tr><td align="right">Current</td>')
        for c in comp:
            out.write('<td align="right">%.1f</td>' % other.times[c].real_m)
        out.write("</tr>\n")
        # Factor
        out.write('<tr><td align="right">Factor</td>')
        for c in comp:
            out.write('<td align="right">%.2f</td>' % ((other.times[c].real_m)/(self.times[c].real_m)))
        out.write("</tr>\n")
        out.write("</table>\n")

memory_list = ['run', 'update']
memory_prefixes = {'run' : 'mem',
                   'update' : 'mem_update'}

class PackageMemory:
    """ Stores the values of highest memory consumption
        for the different prefixes (run/update) of
        a single package.
    """
    def __init__(self):
        self.mems = {}

    def readMemory(self, path):
        # Loop over all known memory_prefixes
        for p in memory_list:
            fpath = os.path.join(path, memory_prefixes[p]+'1.csv')
            if os.path.isfile(fpath):
                self.mems[p] = getHighestMemValue(fpath)

    def renderHtml(self, out):
        # Loop over all known time_list
        out.write("<table border=1>\n")
        out.write("<tr><th>Run</th><th>Maximum [MByte]</th><th>Graph</th></tr>\n")
        for r in memory_list:
            if r in self.mems:
                out.write('<tr><td align="right">%s</td><td align="right">%.1f</td><td align="right"><a href="%s">%s</a></td></tr>\n' % (r,
                          self.mems[r]/1000.0,
                          memory_prefixes[r]+'1.png',
                          memory_prefixes[r]+'1.png'))
        out.write("</table>\n")
        
    def renderCompareHtml(self, other, out):
        # Loop over all known time_list
        out.write("<table border=1>\n")
        out.write("<tr><th>Run</th>")
        comp = []
        for r in memory_list:
            if r in self.mems and r in other.mems:
                comp.append(r)
        # Header line
        for c in comp:
            out.write("<th>%s [MByte]</th>" % c)
        out.write("</tr>\n")
        # Previous run
        out.write('<tr><td align="right">Previous</td>')
        for c in comp:
            out.write('<td align="right">%.1f</td>' % ((self.mems[c])/1000.0))
        out.write("</tr>\n")
        # Current run
        out.write('<tr><td align="right">Current</td>')
        for c in comp:
            out.write('<td align="right">%.1f</td>' % ((other.mems[c])/1000.0))
        out.write("</tr>\n")
        # Factor
        out.write('<tr><td align="right">Factor</td>')
        for c in comp:
            out.write('<td align="right">%.2f</td>' % (float(other.mems[c])/float(self.mems[c])))
        out.write("</tr>\n")
        out.write("</table>\n")
        

def getProfileRunTime(fpath):
    """ Return the total running/profiling time
        for the given pstats file.
    """
    p = pstats.Stats(fpath)

    return p.total_tt

profile_list = ['run', 'update', 'update_implicit']
profile_prefixes = {'run' : 'prof',
                    'update' : 'prof_update',
                    'update_implicit' : 'prof_update_implicit'}

class FolderInfo:
    def __init__(self):
        self.times = None
        self.proftime = {}
        self.memory = None
        
    def readInfos(self, path):
        if os.path.isdir(path):
            ti = PackageTimes()
            ti.readTimes(path)
            self.times = ti
            mi = PackageMemory()
            mi.readMemory(path)
            self.memory = mi
            # Read profile results
            for key in profile_list:
                fpath = os.path.join(path, profile_prefixes[key]+'1.results')
                if os.path.isfile(fpath):
                    self.proftime[key] = getProfileRunTime(fpath)
                    
    def renderHtml(self, out):
        if self.times:
            out.write("<h2>Times</h2>\n")
            self.times.renderHtml(out)
        if self.memory:
            out.write("<h2>Memory</h2>\n")
            self.memory.renderHtml(out)
        if self.proftime:
            out.write("<h2>Profiling</h2>\n")
            out.write("<table border=1>\n")
            out.write("<tr><th>Run</th><th>Total time [s]</th><th>Graphs</th></tr>\n")
            # Output profile results
            for p in profile_list:
                if p in self.proftime:
                    out.write('<tr><td align="right">%s</td><td align="right">%.1f</td><td align="right"><a href="%s1.svg">SVG</a>, <a href="%s1.png">PNG</a></td></tr>\n' % (p,
                                             self.proftime[p],
                                             profile_prefixes[p],
                                             profile_prefixes[p]))
            out.write("</table>\n")
            
    def renderCompareHtml(self, other, out):
        if self.times and other.times:
            out.write("<h3>Times</h3>\n")
            self.times.renderCompareHtml(other.times, out)
        if self.memory and other.memory:
            out.write("<h3>Memory</h3>\n")
            self.memory.renderCompareHtml(other.memory, out)
        if self.proftime and other.proftime:
            out.write("<h3>Profiling</h3>\n")
            out.write("<table border=1>\n")
            
            out.write("<tr><th>Run</th>")
            comp = []
            for p in profile_list:
                if p in self.proftime and p in other.proftime:
                    comp.append(p)
            # Header line
            for c in comp:
                out.write("<th>%s [s]</th>" % c)
            out.write("</tr>\n")
            # Previous run
            out.write('<tr><td align="right">Previous</td>')
            for c in comp:
                out.write('<td align="right">%.1f</td>' % self.proftime[c])
            out.write("</tr>\n")
            # Current run
            out.write('<tr><td align="right">Current</td>')
            for c in comp:
                out.write('<td align="right">%.1f</td>' % other.proftime[c])
            out.write("</tr>\n")
            # Factor
            out.write('<tr><td align="right">Factor</td>')
            for c in comp:
                out.write('<td align="right">%.2f</td>' % ((other.proftime[c])/(self.proftime[c])))
            out.write("</tr>\n")
            out.write("</table>\n")

class RunInfo:
    def __init__(self):
        self.packages = {}
        
    def readInfos(self, path):
        for p in sconstest.packages.keys():
            ppath = os.path.join(path, p)
            if os.path.isdir(ppath):
                fi = FolderInfo()
                fi.readInfos(ppath)
                self.packages[p] = fi

    def renderAllHtmls(self, path):
        for p, val in self.packages.iteritems():
            ipath = os.path.join(path, p, "index.html")
            out = open(ipath, "w")
            out.write("<html>\n")
            out.write("<head>\n")
            out.write("<title>Statistics for %s</title>\n" % p)
            out.write("</head>\n")
            out.write("<body>\n")
            val.renderHtml(out)
            out.write("</body>\n")
            out.write("</html>\n")
            out.close()

    def renderCompareHtml(self, title, other, othertitle, html):
        out = open(html, "w")
        out.write("<html>\n")
        out.write("<head>\n")
        out.write("<title>Comparing %s to %s</title>\n" % (title, othertitle))
        out.write("</head>\n")
        out.write("<body>\n")

        for p, val in self.packages.iteritems():
            if p in other.packages:
                out.write("<h1>%s</h1>\n" % p)
                val.renderCompareHtml(other.packages[p], out)
        
        out.write("</body>\n")
        out.write("</html>\n")
        out.close()

def compare_folders(resultpath, previous, current, html):
    ri_prev = RunInfo()
    ri_prev.readInfos(os.path.join(resultpath, previous))
    ri_cur = RunInfo()
    ri_cur.readInfos(os.path.join(resultpath, current))
    ri_prev.renderCompareHtml(previous, ri_cur, current, html)

def eval_folder(path):
    oldwd = os.path.abspath(os.getcwd())
    os.chdir(path)
    rfiles = glob.glob('*.results')
    for fname in rfiles:
        fstem, ext = os.path.splitext(fname)

        os.system("python %s -f pstats -o %s.dot %s" % (os.path.join(sconstest.suite, 'tools', 'gprof2dot.py'), fstem, fname))
        os.system("cat %s.dot | dot -Tpng -o %s.png" % (fstem, fstem))
        os.system("cat %s.dot | dot -Tsvg -o %s.svg" % (fstem, fstem))

    cfiles = glob.glob('*.csv')
    for fname in cfiles:
        fstem, ext = os.path.splitext(fname)
        title = ''
        for key, val in memory_prefixes.iteritems():
            if fstem.startswith(val) and (len(key) > len(title)):
                title = key

        plotCsvFile(fname, fstem+'.png', title)
    
    os.chdir(oldwd)

def eval_all_folders(path):
    oldwd = os.path.abspath(os.getcwd())
    os.chdir(path)
    for value in sconstest.packages.keys():
        print "  %s" % value
        eval_folder(value)

    os.chdir(oldwd)

    ri = RunInfo()
    ri.readInfos(path)
    ri.renderAllHtmls(path)

def main():
    eval_all_folders('.')

if __name__ == "__main__":
    main()
