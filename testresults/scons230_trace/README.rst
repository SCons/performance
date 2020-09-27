##########################
SCons 2.3.0 trace analysis
##########################

Based on the comparison of `SCons 2.3.0 vs. make` in the parallel ``scons230_vs_make``
folder, this directory contains the run scripts and results of the follow-up
analysis with ``strace``.
All together, it tries to document an in-depth look at the runtime behaviour of SCons,
and even Python processes in general.

Contents
########

The single folders represent the different phases of the experiments, and were
carried out in the following order:

    ``fastcpp``
        Development of the ``fastcpp`` Tool, and first results for this
        new builder.
    ``strace``
        Analysis of SCons runtime behaviour with ``strace``, for CPython and PyPy.
    ``batchbuild``
        Development of the ``batchcompile`` Tool, and first results for this
        new builder.
    ``stubprocess``
        First version of the ``stubprocess.py`` wrapper, and results for this
        subprocess replacement.
    ``stubprocess_patched``
        Results for the stubprocess wrapper, when run on the questfperf
        example with patched sources (extended the classes by some methods
        using STL templates).



Running things
##############

All the scripts looping over the single projects, running
the builds and collecting the timing infos, rely on the
``sconstest`` package available at
https://github.com/SCons/scons-performance/tree/master/testsuite. 

Machines
########

For the basic trace analyis in the folder ``strace`` the following system was used:

  * 2 Intel(R) Core(TM)2 Duo CPU E8300  @ 2.83GHz
  * 2 GB RAM
  * Ubuntu Linux 12.04.02 LTS (x86-64)
  * make 3.81
  * gcc 4.6.3
  * python 2.7.3

All the larger benchmarks (folders ``fastcpp``, ``batchbuild`` and ``stubprocess``) 
were carried out on a:

  * 4 AMD A8-5600K APU @ 1.4GHz
  * 8 GB RAM
  * Ubuntu Linux 12.04.02 LTS (x86-64)
  * make 3.81
  * gcc 4.6.3
  * python 2.7.3


