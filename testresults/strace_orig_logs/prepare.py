import os

os.system('./scons_test.pl')
for pattern in ['SConstruct','SConscript','Makefile']
    os.system('cd sconsbld; find . -name "%s" -exec rm {} ;' % pattern)

projs = ['1_cpython',
         '2_pypy',
         '3_os_spawn',
         '4_direct_touch']

for p in projs:
    os.system('cp -R ./sconsbld %s' % os.path.join(p, 'sconsbld'))

