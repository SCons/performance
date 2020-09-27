#####################
Testresults for SCons
#####################

Welcome to the SCons testresults. This folder is a collection of several
run time analysis and profilings of real-life projects and artificial benchmarks
using SCons (http://www.scons.org).
The scripts for automatically timing and profiling single builds
and update runs, rely on the accompanying ``testsuite`` folder
which is available at https://github.com/SCons/scons-performance too.
Its purpose is to be able to compare different SCons revisions
regarding time and memory consumption.

**Disclaimer**: The testsuite mentioned above was developed during my analysis
of SCons' runtime behaviour for the Wiki article "Why SCons is not slow"
( https://github.com/SCons/scons/wiki/WhySconsIsNotSlow ). It's currently not
in a state of "running everywhere", but especially crafted for my very own Ubuntu
Linux machine.
So, if you try to start the examples on your own, be prepared to run into
some pitfalls. You might have to adapt the controlling scripts, or even need
to patch the software packages themselves...including the installation of
special packages as prerequisites.

Contents
########

    ``scons120_vs_make``
        Based on a test benchmark by Eric Melski, the somewhat ancient
        SCons v1.2.0 is run and compared against the classical `make`.
    ``scons230_vs_make``
        Here a current SCons v2.3.0 is used, and not only run on a single
        core/CPU but also in parallel. Additionally, the underlying `wonderbuild`
        and `Quest for performance` benchmarks get patched, such that
        the CPP compiler gets some real work to do.
    ``scons230_trace``
        Following the comparison of make vs SCons above, this folder
        documents an analysis with ``strace``. Three builders and extensions, 
        ``fastcpp``, ``batchbuild`` and ``stubprocess``, got developed for
        speeding up large clean and update builds.
    ``testsuite``
        Results for several runs of the full `scons_testsuite` against special
        SCons experimental development branches.
    ``strace_orig_logs``
        Detailed tracings of single compile commands for CPython and PyPy.

In each of the above listed result folders, you'll find a reST file named something
like `README.rst` or `overview.rst`. It explains the structure and contents of each
comparison in greater detail.

