import os

os.system('./scons_test.pl')
for pattern in ['SConstruct','SConscript','Makefile']
    os.system('cd sconsbld; find . -name "%s" -exec rm {} ;' % pattern)

projs = ['cpython',
         'pypy']

for p in projs:
    os.system('cp -R ./sconsbld %s' % os.path.join(p, 'sconsbld'))

