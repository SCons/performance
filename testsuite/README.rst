###################
Testsuite for SCons
###################

Welcome to the SCons testsuite. This folder is a collection of several
real-life projects and artificial benchmarks using SCons (http://www.scons.org).
Together with some scripts for automatically timing and profiling single builds
and update runs, its purpose is to be able to compare different SCons revisions
regarding time and memory consumption.

**Disclaimer**: This testsuite was developed during my analysis of SCons' runtime
behaviour for the Wiki article "Why SCons is not slow". It's currently not
in a state of "running everywhere", but especially crafted for my very own Ubuntu
Linux machine.
So, if you try to start the examples on your own, be prepared to run into
some pitfalls. You might have to adapt the controlling scripts, or even need
to patch the software packages themselves...including the installation of
special packages as prerequisites.

Contents
########

    ``packages``
        Contains the source packages for the example projects in
        various formats like ``.zip`` or ``.tgz``.
    ``src``
        A simple Python package named ``sconstest``, providing
        some basic helper and support routines.
    ``tools``
        A copy of ``gprof2dot.py`` and two wrapper scripts for
        profiling SCons runs.
    ``.``
        The basic shell and Python scripts for running single tests
        or evaluating and comparing the results, respectively.

Configuring and installing
##########################

For being able to run any tests, you have to install the ``sconstest`` package,
but need to configure some paths beforehand.
At the top of the file ``src/sconstest/__init__.py``, change the three variables

    ``suite``
        Absolute path, pointing to the folder where your copy of the sconstest
        repository is located. Example: ``/home/dirk/workspace/scons_testsuite``
    ``sconswd``
        Absolute path, pointing to the ``src`` folder of the SCons version
        that you want to test. Example: ``/home/dirk/workspace/scons_experimental/src``
    ``results``
        Relative path, the name of the folder where all results of the single
        runs get stored. Example: ``results`` 
    
according to your local setup.

Then issue the command::

    sudo python setup.py install
    
.

Running a test
##############

There are three basic types of tests that you can run:

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

The scripts ``all_suite_fast.sh`` and ``all_suite.sh`` combine all these three
tests, while the latter runs each ``time`` test three times and mediates all
results accordingly.

For each of the three test types, there exists a ``_run.py`` and a ``_single.py``
version. While the ``_run.py`` version loop over all defined project packages
and get started from the ``scons_testsuite`` folder itself, the ``_single.py``
scripts get called from the actual source folders for each project.

For the result folder structure it's assumed that you want to compare
different source changes, or revisions, for a single SCons version. That's
why the ``results`` folder is somewhat hardcoded into the test framework.
Within this ``results`` folder the single runs get a separate subdirectory each.
For example if you call::

    ./all_suite_fast.sh changed
    
this will create a ``results/changed`` folder with all the results of all
project packages inside, based on the current source code of the SCons version
that you specified via the ``sconswd`` variable.

Before starting any project builds or tests manually, you'll want to call::

    python prepare.py
    
, which creates the subfolder ``build`` for you and unpacks all source packages
for the examples to it.

Evaluating results
##################

This is actually done automatically on a call of the ``all_suite*`` scripts.
However, you can also call the script ``eval_all.py`` manually as::

    python eval_all.py default
    
, which will dive into the current ``results`` folder and create PNG and SVG images
for the profiling results.

Comparing different runs
########################

Once you collected the results of different changes, you might want to compare
their results against the original state, in order to check for
significant speedups.

We assume that you ran a full test of your original source state as ``default``,
and you have some new results for your changed sources in the folder ``changed``.
Then you can create a simple HTML file with the command::

    python compare_runs.py default changed
    
    
. It gets written as ``comparison.html`` to the ``changed`` folder.
 
