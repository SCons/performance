
"""SCons.Tool.batchcompile

A Tool for batch compiling C/CPP files, intended to speed up clean
builds in large projects.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""

#
# Copyright (c) 2001-7,2010,2011,2012,2013,2014 The SCons Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import os
import subprocess
import tempfile

import SCons.Builder
import SCons.Util


def _batch_compile(target, source, env):
    tfile = tempfile.NamedTemporaryFile(mode="w", suffix='.sh', delete=False)
    idx = 0
    for t, s in zip(target, source):
        head, tail = os.path.splitext(str(s))
        if head:
            # Write command into shell file
            cmd = env.subst('$CCCOM', 0, t, s)
            cmdstr = env.subst('$CCCOMSTR', 0, t, s)
            if not cmdstr:
                cmdstr = cmd
            tfile.file.write('echo "%s" && \\\n' % cmdstr)
            if (idx+1) < len(source):
                tfile.file.write('%s && \\\n' % cmd)
            else:
                tfile.file.write('%s\n' % cmd)
        idx += 1
    tfile.close()

    ENV = env['ENV']

    # Ensure that the ENV values are all strings:
    for key, value in ENV.items():
        if not SCons.Util.is_String(value):
            if SCons.Util.is_List(value):
                # If the value is a list, then we assume it is a
                # path list, because that's a pretty common list-like
                # value to stick in an environment variable:
                value = SCons.Util.flatten_sequence(value)
                ENV[key] = os.pathsep.join(map(str, value))
            else:
                # If it isn't a string or a list, then we just coerce
                # it to a string, which is the proper way to handle
                # Dir and File instances and will produce something
                # reasonable for just about everything else:
                ENV[key] = str(value)

    # Call subprocess
    proc = subprocess.Popen(". %s" % tfile.name, env = ENV, close_fds = True, shell=True)
    res = proc.wait() 
    os.unlink(tfile.name)

    return res

#
# Builders
#
_batch_builder = SCons.Builder.Builder(
        action = _batch_compile,
        zipdep = True)


def BatchCompileC(env, target, source=None, *args, **kw):
    """
    A pseudo-Builder wrapper for compiling C files in a batch.
    """
    if not SCons.Util.is_List(target):
        target = [target]
    if not source:
        source = target
    if not SCons.Util.is_List(source):
        source = [source]

    result = []
    # Process list of sources in steps
    # of the current batch size each.
    batch_len = 1000
    try:
        batch_len = int(env.subst("BCC_BATCH_SIZE"))
    except:
        pass
    if batch_len < 2:
    	return env.StaticObject(target, source)

    steps, remainder = divmod(len(source), batch_len)
    objsuffix = env.subst("$OBJSUFFIX")
    for i in xrange(steps):
        targets = []
        for s in source[i*batch_len:(i+1)*batch_len]:
            head, tail = os.path.splitext(str(s))
            t = env.File(head+objsuffix)
            targets.append(t)
        objs = _batch_builder.__call__(env, targets, source[i*batch_len:(i+1)*batch_len], **kw)
        result.extend(objs)

    # Process final slice of sources
    targets = []
    for s in source[-remainder:]:
        head, tail = os.path.splitext(str(s))
        t = env.File(head+objsuffix)
        targets.append(t)
    objs = _batch_builder.__call__(env, targets, source[-remainder:], **kw)
    result.extend(objs)
    
    return result


def generate(env):
    """Add Builders and construction variables to the Environment."""

    env.SetDefault(
        BCC_BATCH_SIZE = '50'
    )
    try:
        env.AddMethod(BatchCompileC, "BatchCompileC")
    except AttributeError:
        # Looks like we use a pre-0.98 version of SCons...
        from SCons.Script.SConscript import SConsEnvironment
        SConsEnvironment.BatchCompileC = BatchCompileC


def exists(env):
    return 1

