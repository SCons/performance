##########################
Trace runs for SCons 2.3.0
##########################

This folder contains the run scripts and results of several
experiments with "strace".

Special changes
###############

For reducing clutter in the output of the ``strace`` command, a few
changes were made to the original SCons version and the
benchmark scripts:

 * The standard SHELL in SCons was set to the more lightweight ``dash``,
   instead of ``bash``.
 * A single environment is setup in the benchmark scripts, that gets
   exported to the build files in the subdirectories. 
 * The ``tools`` variable for the ``DefaultEnvironment`` is set empty,
   such that a minimal amount of time is wasted to search for available tools.
 * The actual build commands for the compiler, linker and such are replaced
   by ``echo`` instructions. So no real executable is called, but only
   the command gets printed to ``stdout``.
 
Basic execution
###############

For each of the result folders, SCons was run via the command::

    strace -o out.txt -r -f -s 256 scons

. The resulting text output file (not included in the repo because
it's too large) with the single trace lines was then
searched for two single compile operations (``*.c -> *.o``). One
at the start of the build (``first.txt``), and one close to the end
(``second.txt``). 

With the script ``accu_times.py`` one can then convert each text file into
a CSV, containing the accumulated time for each single compile over the
number of steps (=syscalls).

By comparing the two times (``runtimes.png``), one can see that the number of steps are equal.
But the second invocation has one (or sometimes two) dedicated jumps, accounting for
a larger time per compile command to the end of the build. 
When comparing the log outputs for the steps in question, one can find
that it's the ``mmremap`` or ``wait`` creating the overhead in time.

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

Machine
#######

For the runs under Linux the following system was used:

  * 2 Intel(R) Core(TM)2 Duo CPU E8300  @ 2.83GHz
  * 2 GB RAM
  * Ubuntu Linux 12.04.02 LTS (x86-64)
  * make 3.81
  * gcc 4.6.3
  * python 2.7.3

