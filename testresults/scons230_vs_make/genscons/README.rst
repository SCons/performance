#####################
SCons 2.3.0 vs v1.2.0
#####################

This folder contains the run scripts and results of a runtime
comparison between SCons v2.3.0 and the much older v1.2.0 for
the genscons.pl benchmark script.

Contents
########

    ``b, c, d, e``
        The original Perl setup script for the test benchmark, in
        different project sizes ranging from 2500 up to 16500 C files.
    ``results``
        The timing results of the single results, you can find a
        files-time diagram in the ``all`` subfolder for clean
        builds and updates each.
    ``time_all.py``
        The main script that loops over all single projects, runs
        the builds and collects the timing infos.
        Requires the ``sconstest`` package from
        https://github.com/SCons/scons-performance/tree/master/testsuite. 

Project sizes
#############

Sizes of the single projects are::

    b = 2500 C files
    c = 4500 C files
    d = 8500 C files
    e = 16500 C files

Machine
#######

For the runs under Linux the following system was used:

  * 2 Intel(R) Core(TM)2 Duo CPU E8300  @ 2.83GHz
  * 2 GB RAM
  * Ubuntu Linux 12.04.02 LTS (x86-64)
  * make 3.81
  * gcc 4.6.3
  * python 2.7.3

