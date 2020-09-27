###################
SCons 2.3.0 vs make
###################

This folder contains the run scripts and results of several runtime
comparisons between SCons v2.3.0 and the make tool.

Contents
########

    ``genscons``
        Project setup and results of a comparison between SCons 2.3.0 and the much older
        SCons 1.2.0 for the `genscons.pl` benchmark.
    ``questfperf``
        Project setup and results of the `Quest for performance` benchmark.
    ``wonderbuild``
        Project setup and results of the `wonderbuild` benchmark.
    ``parallel``
        In this project, SCons was compared to make on quad and octa
        machines, while using the ``-j`` option for running build
        steps in parallel.


Running things
##############

All the scripts looping over the single projects, running
the builds and collecting the timing infos, rely on the
``sconstest`` package available at
https://github.com/SCons/scons-performance/tree/master/testsuite. 

Machines
########

For all the benchmarks (except the subfolder `parallel`) the following system was used:

  * 2 Intel(R) Core(TM)2 Duo CPU E8300  @ 2.83GHz
  * 2 GB RAM
  * Ubuntu Linux 12.04.02 LTS (x86-64)
  * make 3.81
  * gcc 4.6.3
  * python 2.7.3

In the folder `parallel`, the `quad_core` configuration used a:

  * 4  Intel(R) Core(TM) i5 CPU 650  @ 3.20GHz
  * 4 GB RAM
  * SLES11 SP2, 32bit
  * Kernel 3.0.13-0.27-pae

and the `octa_core` comparisons were carried out on a:

  * 8 Intel(R) Xeon(R) CPU X3460  @ 2.80GHz
  * 4 GB RAM
  * SLES10 SP3, 32bit
  * Kernel 2.6.16.60-0.54.5-bigsmp

