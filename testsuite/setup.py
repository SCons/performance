#!/usr/bin/env python

from distutils.core import setup

setup(name='sconstest',
      version='1.0',
      description='Utils for the SCons testsuite',
      author='Dirk Baechle',
      author_email='dl9obn@darc.de',
      url='https://github.com/SCons/scons-performance',
      packages=['sconstest'
               ],
      package_dir={'' : 'src'},
      scripts = ['tools/lscons','tools/lscons_cprofile']
     )

