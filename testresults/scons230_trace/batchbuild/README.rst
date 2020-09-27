#######################
SCons batchcompile Tool
#######################

As as first fix for the ``fork`` problem, a simple Batch builder was developed.
It's able to compile C files in a batch, by writing a temporary shell script "on the fly"
and then calling it. 
Find a first version in the ``batchcompile`` folder...together with a required patch to the
``Builder.py`` source. The new Builder option "zipdep" allows SCons to generate a simple 1:1
dependency between each target and source, instead of the default 1:n. 

Contents
########

The single folders contain the results for the following runs:

    ``batchcompile``
        First version of the ``batchcompile`` Tool.
    ``single_core``
        Running SCons with the new builder, and on one core only.
    ``parallel_j4``
        Testing the batch builder against the ``-j4`` option.

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

