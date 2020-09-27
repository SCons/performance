==============================================
Overview of the "Quest for performance" builds
==============================================


Folders
-------

results*
    Timing results for the single SCons and make runs with the
    `-j` option.
graph*.py and plot_all.py
    Helper scripts to create the result graphs in the `scaling`
    and `speedup` folders.
run_all.sh and time_all.py
    Wrapper scripts for running the whole bunch of different
    configurations in one swoop.
scaling
    Result graphs in PNG format, showing the run times (clean build
    and update) over the number of CPP files for each `-j` option.
speedup
    Here the graphs display the speedup over the number of cores.
    This evaluation was done for each project size (from `small`
    to `vvlarge`) for clean builds only, since SCons doesn't do
    updates in parallel.
 
Project sizes
-------------

Sizes of the single projects are::

    small   =  5000 CPP files
    middle  = 10000 CPP files
    large   = 20000 CPP files
    vlarge  = 30000 CPP files
    vvlarge = 40000 CPP files

Results
-------

In each of the *results* folders, you can find the
time and profiling results for the single steps,
from `small`, via `middle` and `large`, `vlarge` to `vvlarge`.

Where applicable the *SCons* results are prefixed with `scons_` and *make*
gets the prefix `make_`.

The meaning of the suffixes is:

`cleanbuild`
    Build from scratch.
`update`
    Update, right after a clean build, without any source changes.
`update_implicit`
    Update like above, using the `--max-drift=1 --implicit-deps-unchanged`
    parameters for speedup (*SCons* only).

In the `scaling` and `speedup` subdirectories you can find the resulting graphs
for clean builds and update runs as PNG files. These files got prepared directly
from the timing results (`*.times`)
by the `graph_scaling.py` and `graph_parallel_speedup.py` scripts.

