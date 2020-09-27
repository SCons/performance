###################
SCons 2.3.0 vs make
###################

This folder contains the run scripts and results of several runtime
comparisons between SCons v2.3.0 and the make tool.

Contents
########

    ``quad_core``
        Project setups and results as run on a quad core machine.
    ``octa_core``
        Project setups and results that were run on a octa core setup.


Running things
##############

All the scripts looping over the single projects, running
the builds and collecting the timing infos, rely on the
``sconstest`` package available at
https://github.com/SCons/scons-performance/tree/master/testsuite.

Machines
########

The `quad_core` configuration used a:

  * 4  Intel(R) Core(TM) i5 CPU 650  @ 3.20GHz
  * 4 GB RAM
  * SLES11 SP2, 32bit
  * Kernel 3.0.13-0.27-pae

and the `octa_core` comparisons were carried out on a:

  * 8 Intel(R) Xeon(R) CPU X3460  @ 2.80GHz
  * 4 GB RAM
  * SLES10 SP3, 32bit
  * Kernel 2.6.16.60-0.54.5-bigsmp

