################################
SCons 2.3.0 analysis with strace
################################

Led by Eric Melski's remarks in his latest article
http://blog.melski.net/2013/12/11/update-scons-is-still-really-slow/
, I was finally able to reproduce his results on a larger machine with 8GB RAM.
The results, graphs and figures in this folder are all based on a simplified version
of the benchmark, where the actual compiler and linker calls are replaced by the
"``echo``" command. This means faster runtimes for the program and the benchmarks,
while still showing the same basic behaviour.

Contents
########

    ``pypy_vs_cpython``
        Running builds of SCons and comparing the runtimes between CPython and PyPy.
    ``pypy_cpython_touch_only``
        Running builds with a patched version of SCons and comparing CPython and PyPy.
        The patch (see file ``action.patch``) replaces the actual spawn of a subprocess
        with a direct touch of the target file. This is done in Python directly, by
        opening a file and then closing it immediately.
    ``tracings``
        Results of running SCons through the ``strace`` command.
    ``test_prog``
        Test programs for the basic runtime behaviour of the fork calls on
        system level. A Python and C version are provided.


Running things
##############

All the scripts looping over the single projects, running
the builds and collecting the timing infos, rely on the
``sconstest`` package available at
https://github.com/SCons/scons-performance/tree/master/testsuite. 

Machines
########

For the basic trace analyis in the folder ``tracings`` the following system was used:

  * 2 Intel(R) Core(TM)2 Duo CPU E8300  @ 2.83GHz
  * 2 GB RAM
  * Ubuntu Linux 12.04.02 LTS (x86-64)
  * make 3.81
  * gcc 4.6.3
  * python 2.7.3

All the larger benchmarks (folders ``pypy_vs_cpython`` and ``pypy_cpython_touch_only``) were carried out on a:

  * 4 AMD A8-5600K APU @ 1.4GHz
  * 8 GB RAM
  * Ubuntu Linux 12.04.02 LTS (x86-64)
  * make 3.81
  * gcc 4.6.3
  * python 2.7.3


