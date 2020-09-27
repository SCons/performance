===============================================
Overview of the "Wonderbuild" benchmark results
===============================================


Folders
-------

rsc
    Files and archives as downloaded originally from the Internet.
    (URL: http://www.retropaganda.info/~bohan/work/psycle/branches/bohan/wonderbuild/benchmarks/time.xml )
run_original
    Results for unchanged build scripts.
run_patched
    Results for builds with some methods and includes added to the test
    files, such that the compiler has actually some work to do.

Project sizes
-------------

Sizes of the single projects are::

    small  =  5000 CPP files
    middle = 10000 CPP files
    large  = 12500 CPP files
    vlarge = 15000 CPP files

Results
-------

In each of the *run* folders from above, you can find a `results` subdirectory.
It keeps the time and profiling results for the single steps,
from `small`, via `middle` and `large`, to `vlarge`.

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

In the `all` subdirectories you can find the resulting graphs for clean builds and update
runs as PNG files. These files got prepared directly from the timing results (`*.times`)
by the `graph_scaling.py` script.

