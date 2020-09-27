# Paths to commands and working directories

suite = "/home/dirk/workspace/scons_testsuite"
sconswd = "/home/dirk/workspace/scons_experimental/src"
results = "results"

#
# You shouldn't have to edit
# something below here...
#
lscons = suite + "/tools/lscons"
lsconsprof = suite + "/tools/lscons_cprofile"
redirect = " > /dev/null 2>&1"
perc = '%'
time = "/usr/bin/time -f \"%sE, %sU, %sS\"" % (perc, perc, perc)

packages = {'ascend'      : {'path' : 'ascend-0.9.7',
                             'archive' : 'my_ascend-0.9.7.tar'},
            'bombono'     : {'path' : 'bombono-dvd-1.2.2',
                             'archive' : 'my_bombono.tar'},
            'lumiera'     : {'path' : 'LUMIERA',
                             'archive' : 'LUMIERA.tgz', 
                             'optargs' : ' ARCHFLAGS="-DBOOST_FILESYSTEM_VERSION=2"'},
            'mapnik'      : {'path' : 'mapnik-v2.0.1',
                             'archive' : 'mapnik-v2.0.1.tar'},
            'sconsbld'    : {'path' : 'sconsbld',
                             'archive' : 'sconsbld.tar'},
            'wonderbuild' : {'path' : 'wonderbuild',
                             'archive' : 'wonderbuild.tgz'},
            'questfperf'  : {'path' : 'questfperf',
                             'archive' : 'questfperf.tgz'}
           }
