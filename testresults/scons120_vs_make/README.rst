###################
SCons 1.2.0 vs make
###################

This folder contains the run scripts and results of a runtime
comparison between SCons v1.2.0 and the make tool.

Contents
########

    ``b, c, d, e``
        The original Perl setup script for the test benchmark, in
        different project sizes ranging from 2500 up to 16500 C files.
    ``results``
        The timing results of the single results, you can find a
        files-time diagram in the ``all`` subfolder for clean
        builds and updates each.
        The project sizes ``d`` and ``e`` also contain profiling
        results in PNG and SVG formats, allowing a comparison
        of how the single portions of SCons allocate parts of
        the total runtime.
    ``results_windows``
        The timings above were repeated under Windows, to ensure
        that the reported allegedly quadratic behaviour isn't OS specific.
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

Machines
########

For the runs under Linux the following system was used:

  * 2 Intel(R) Core(TM)2 Duo CPU E8300  @ 2.83GHz
  * 2 GB RAM
  * Ubuntu Linux 12.04.02 LTS (x86-64)
  * make 3.81
  * gcc 4.6.3
  * python 2.7.3

The comparisons for Windows were performed on a:

  * AMD Sempron 2600+ @ 1.6GHz
  * 4 GB RAM
  * Windows XP, Home Edition, 32bit
  * mingw-32 v4.6.2
  * Python 2.7.2
  * ptime 1.0
  * Perl 5.16.3 (ActiveState)


