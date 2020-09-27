##################
SCons fastcpp Tool
##################

In general, the running time of SCons is distributed over a lot of different modules and
functions, making it difficult to identify a single place that is suited for optimization.
However, by cycling through patching the source code and rerunning the tests I found two
places where a lot of time gets spent on the wrong things in my opinion.
At least this is where we could spare a few cycles, especially for large projects with a
lot of C/CPP files:

 1. The prefixes and suffixes for programs, objects and libraries in the default C/CPP
 builders are set as variables. This means that they have to get substituted every time
 a corresponding target gets built.

 2. Somewhat related to this is the flexibility that we offer when specifiying
 C/CPP source files. By adding a large list of different scanners for file suffixes, 
 we have to check against them for each source file we encounter. When a user knows that
 he only has CPP files to process, there is simply no need to check for FORTRAN...

These observations have led to the development of another external Tool called "fastcpp".
It's available in the scons-contrib repo ( https://github.com/SCons/scons-contrib ) and can be loaded on
top of a normal C/CPP building environment.


Contents
########

The single folders contain the results for the following runs:

    ``reference``
        Run of SCons without speeding up anything at all, for getting reference times that
        we can compare against the following tests.
    ``fullbuild``
        Comparison of make vs SCons with the ``fastcpp`` builder.
    ``single_dir``
        Updating a single library folder only, with the ``fastcpp`` builder.
    ``single_dir_notool``
        Updating a single library folder only, without the ``fastcpp`` builder.


Running things
##############

All the scripts looping over the single projects, running
the builds and collecting the timing infos, rely on the
``sconstest`` package available at
https://github.com/SCons/scons-performance/tree/master/testsuite. 

Machines
########

All the builds were run on a:

  * 4 AMD A8-5600K APU @ 1.4GHz
  * 8 GB RAM
  * Ubuntu Linux 12.04.02 LTS (x86-64)
  * make 3.81
  * gcc 4.6.3
  * python 2.7.3

