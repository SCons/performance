#################################
SCons 2.3.0, PyPy, simplified run
#################################

Running times for SCons runs in PyPy with a simplified version
of the ``genscons.pl`` benchmark script.
All the actual compiler and linker calls are replaced by the
"``echo``" command. This means faster runtimes for the program and the benchmarks,
while still showing the same basic behaviour.

Contents
########

    ``f-p``
        The original Perl setup script for the test benchmark, in
        different project sizes.
    ``results``
        The timing results of the single results, you can find
        files-time diagrams in the ``all`` subfolder for clean
        builds and updates each.
    ``time_all.py``
        The main script that loops over all single projects, runs
        the builds and collects the timing infos.
        Requires the ``sconstest`` package from
        https://github.com/SCons/scons-performance/tree/master/testsuite. 

Machine
#######

For the runs under Linux the following system was used:

  * 4 AMD A8-5600K APU @ 1.4GHz
  * 8 GB RAM
  * Ubuntu Linux 12.04.02 LTS (x86-64)
  * make 3.81
  * gcc 4.6.3
  * python 2.7.3

