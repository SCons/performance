###########################
Strace runs for SCons 2.3.0
###########################

This folder contains the run scripts and results of running
SCons through "strace", once for the CPython interpreter and for
PyPy each.

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
 
This why there is a prepared folder ``sconsbld`` in each subfolder, with all
the SConstruct/SConscript files inside.
The script ``prepare.py`` populates the projects with the required C/H files,
if you want to try and rerun the builds on your machine.

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

By comparing the two times (``times.png``, as created by ``graph_time.py``),
one can see that the number of steps are equal.
But the second invocation has several dedicated jumps, accounting for
a larger time per compile command to the end of the build. 
When comparing the log outputs for the steps in question, one can find
that it's the ``mmremap`` or ``wait``, creating the overhead in time.

Contents
########

    ``cpython``
        Result files for the cpython run.
    ``pypy``
        Result files for the pypy run.
    ``accu_times.py``
        Simple script that reads a log snippet file, adds up the
        execution times of the single syscalls and writes them
        to stdout in CSV format.
    ``prepare.py``
        Script for bootstrapping the sconsbld folders in the
        two project directories. (see "Special changes" above)

Machine
#######

For the runs under Linux the following system was used:

  * 2 Intel(R) Core(TM)2 Duo CPU E8300  @ 2.83GHz
  * 2 GB RAM
  * Ubuntu Linux 12.04.02 LTS (x86-64)
  * make 3.81
  * gcc 4.6.3
  * python 2.7.3

