#####################
Testresults for SCons
#####################

This folder contains results for a collection of several
run time analysis and profilings of real-life projects and artificial benchmarks
using SCons (http://www.scons.org).

A base revision of the latest SCons v2.3.0 trunk is compared against
two ideas for further development of the source code.

The scripts for automatically timing and profiling single builds
and update runs, rely on the accompanying ``scons_testsuite`` repository
which is available at https://github.com/SCons/scons-performance/tree/master/testsuite.

**Disclaimer**: The testsuite mentioned above was developed during my analysis
of SCons' runtime behaviour for the Wiki article "Why SCons is not slow". It's currently not
in a state of "running everywhere", but especially crafted for my very own Ubuntu
Linux machine.
So, if you try to start the examples on your own, be prepared to run into
some pitfalls. You might have to adapt the controlling scripts, or even need
to patch the software packages themselves...including the installation of
special packages as prerequisites.

Contents
########

    ``default``
        Based on a fixed revision of the SCons trunk
        these results serve as reference for the following two comparisons.
    ``action_fixext``
        Tries to reduce run times for updates in larger software
        projects with a lot of C/CPP files.
        This is done by using fixed strings for lib and object file
        prefixes/suffixes, instead of the OS-independent variables
        like `$LIBSUFFIX`.
    ``envcache``
        A first try at caching the results of the env.subst() function,
        where possible.


In each of the above listed result folders you'll find a subdirectory for each
single project of the testsuite. There are real software packages like `mapnik`
or `lumiera`, and also artificial benchmarks created from the `wonderbuild` script
for example.

The single project folders contain a lot of result files, that can be divided into
three main groups for the basic types of tests that are run by the testsuite:

    ``time``
        Simple measuring of the runtime via ``/usr/bin/time``, for
        clean builds and updates. In the case of running the ``all_suite.sh``
        script, each run is repeated three times and the median of all
        values gets calculated automatically.
    ``profile``
        Runs SCons through ``cProfile.py``, in order to get an impression
        about where exactly the larger portions of runtime are spent.
    ``memwatch``
        Starts a separate memory watcher in parallel to SCons. This watcher
        peeks into ``/proc/PID/status`` for the process and writes the currently
        used memory (``VmSize``) into a CSV file every second.

Each project folder has its own `index.html` which displays the most important data
in simple tables and also links the created graphs for the profiling and memory consumption
results.

At the top of the `action_fixext` and `envcache` folders, you can find a `compare.html` each.
It lists the speedup factors for the single runs (and the used memory) against the `default` results.

**Disclaimer**: Regard that some of the results simply don't exist, because the changes break several of the builds.
After all these are no valid and stable patches, but mere ideas. So don't use them for production work!

