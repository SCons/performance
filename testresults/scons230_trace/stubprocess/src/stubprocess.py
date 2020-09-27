'''
We have faced an issue with forking processes on RHEL 5.10.
When parent process consumes a realy big amount of memory fork call becomes very slow
because it needs to copy memory pages from parent to child process.
To overcome the issue we use posix_spawn function. The function calls vfork followed by
execve call. This avoids copying of memory pages and saves time but it also prevents us
from redirecting standard input and output because when it is requested posix_spawn
function uses fork instead of vfork and we have the slowdown again.

To make the IO redirection we do not start a requested sub-process immidiately but
use intermediate python script which redirects the IO. The whole call chain looks like this:

Popen("/foo/bar") -> fork -> execve(["python", __file__]) -> execve("/foo/bar")

All parameters needed for I/O redirection are passed in pickle via temporary file.
'''

import sys
if sys.platform in ('linux2', 'darwin'):
    import types
    import time
    import os
    import cPickle as pickle
    import fcntl
    import errno
    import traceback
    import base64

    try:
        cloexec_flag = fcntl.FD_CLOEXEC
    except AttributeError:
        cloexec_flag = 1

    def _set_cloexec_flag(fd, cloexec=True):
        '''
        Utility function to modify close-on-exec flag of specified file descriptor
        '''
        old = fcntl.fcntl(fd, fcntl.F_GETFD)
        if cloexec:
            fcntl.fcntl(fd, fcntl.F_SETFD, old | cloexec_flag)
        else:
            fcntl.fcntl(fd, fcntl.F_SETFD, old & ~cloexec_flag)

    if __name__ == '__main__':
        try:
            MAXFD = os.sysconf("SC_OPEN_MAX")
        except:
            MAXFD = 256

        try:
            from os import closerange
        except ImportError:
            def _close_fds(but):
                '''
                Closes all open file descriptors
                '''
                for i in xrange(3, MAXFD):
                    try:
                        if i <> but:
                            os.close(i)
                    except:
                        pass
        else:
            def _close_fds(but):
                closerange(3, but)
                closerange(but + 1, MAXFD)

        def do_execv(args=None, executable=None, close_fds=None, cwd=None, env=None,
                shell=None, p2cread=None, p2cwrite=None, c2pread=None, c2pwrite=None,
                errread=None, errwrite=None, errpipe_read=None, errpipe_write=None):
            '''
            The function redirects IO, prepares command-line, sets up environment and
            executes execve function.
            '''
            os.close(errpipe_read)
            _set_cloexec_flag(errpipe_write, True)
            try:

                if isinstance(args, types.StringTypes):
                    args = [args]
                else:
                    args = list(args)

                if shell:
                    args = [executable or "/bin/sh", "-c"] + args

                if executable is None:
                    executable = args[0]

                # Close parent's pipe ends
                for parent_end, child_end in ((p2cwrite, p2cread), (c2pread, c2pwrite),
                        (errread, errwrite)):
                    if parent_end is not None:
                        os.close(parent_end)
                    if child_end is not None:
                        _set_cloexec_flag(True)

                # When duping fds, if there arises a situation
                # where one of the fds is either 0, 1 or 2, it
                # is possible that it is overwritten (#12607).
                if c2pwrite == 0:
                    c2pwrite = os.dup(c2pwrite)
                if errwrite == 0 or errwrite == 1:
                    errwrite = os.dup(errwrite)

                # Dup fds for child
                def _dup2(a, b):
                    # dup2() removes the CLOEXEC flag but
                    # we must do it ourselves if dup2()
                    # would be a no-op (issue #10806).
                    if a == b:
                        _set_cloexec_flag(a, False)
                    elif a is not None:
                        os.dup2(a, b)
                _dup2(p2cread, 0)
                _dup2(c2pwrite, 1)
                _dup2(errwrite, 2)

                # Close pipe fds.  Make sure we don't close the
                # same fd more than once, or standard fds.
                closed = set([ None ])
                for fd in [p2cread, c2pwrite, errwrite]:
                    if fd not in closed and fd > 2:
                        os.close(fd)
                        closed.add(fd)

                # Close all other fds, if asked for
                if close_fds:
                    _close_fds(errpipe_write)

                if cwd is not None:
                    os.chdir(cwd)

                if env is None:
                    os.execvp(executable, args)
                else:
                    os.execvpe(executable, args, env)
            except:
                exc_type, exc_value, tb = sys.exc_info()
                # Save the traceback and attach it to the exception object
                exc_lines = traceback.format_exc()
                exc_value.child_traceback = ''.join(exc_lines)
                os.write(errpipe_write, pickle.dumps(exc_value))

            # This exitcode won't be reported to applications, so it
            # really doesn't matter what we return.
            os._exit(255)

        if sys.argv[1] == '@':
            with open(sys.argv[2], 'rb') as data:
                data = data.read()
            os.unlink(sys.argv[2])
        else:
            data = sys.argv[1]
        params = pickle.loads(base64.decodestring(data))
        do_execv(**params)

    else: # __name__ <> '__main__'
        import ctypes
        import tempfile

        try:
            ARG_MAX = os.sysconf('SC_ARG_MAX')
        except:
            ARG_MAX = 32768

        try:
            from subprocess import _eintr_retry_call
        except ImportError:
            def _eintr_retry_call(func, *args, **kw):
                while True:
                    try:
                        return func(*args, **kw)
                    except OSError, err:
                        if err.errno == errno.EINTR:
                            continue
                        raise


        try:
            # We support only Linux and Mac OS X now.
            libc = ctypes.CDLL("libc.so.6" if 'linux' in sys.platform else 'libc.dylib', use_errno=True)
            posix_spawn = libc.posix_spawn
        except (OSError, AttributeError):
            # OSError is raised when no libc.so.6 is found on the system
            # AttributeError is raised when no posix_spawn function can be found
            pass
        else:
            posix_spawn.restype = ctypes.c_int
            posix_spawn.argtypes = (
                    ctypes.POINTER(ctypes.c_int), # ppid
                    ctypes.c_char_p, # executable
                    ctypes.c_void_p, # file_actions
                    ctypes.c_void_p, # attrp
                    ctypes.POINTER(ctypes.c_char_p), #argv
                    ctypes.POINTER(ctypes.c_char_p), #env
            )


            # In Python older than 2.7.6 subprocess.Popen._execute_child accepts 17 arguments.
            # In Python 2.7.6 it accepts 18 args.
            # To workaround the issue we use _unpack_args* functions. Both 27 and 276 return
            # a tuple containing args in order they are passed to Python 2.7.6 _execute_child
            # function. 

            def _unpack_args_27(args):
                result = (self, argv, executable, preexec_fn, close_fds,
                                       cwd, env, universal_newlines,
                                       startupinfo, creationflags, shell, to_close,
                                       p2cread, p2cwrite,
                                       c2pread, c2pwrite,
                                       errread, errwrite) = args[:11] + (set(),) + args[11:]
                to_close.update((p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite))
                return result

            def _unpack_args_276(args):
                try:
                    result = (self, argv, executable, preexec_fn, close_fds,
                                       cwd, env, universal_newlines,
                                       startupinfo, creationflags, shell, to_close,
                                       p2cread, p2cwrite,
                                       c2pread, c2pwrite,
                                       errread, errwrite) = args
                except ValueError:
                    global _unpack_args
                    _unpack_args = _unpack_args_27
                    return _unpack_args_27(args)
                else:
                    return result

            _unpack_args = _unpack_args_276

            def _close_in_parent(fd, to_close):
                os.close(fd)
                to_close.remove(fd)

            def _wrap_execute_child(klass):
                wrapped_execute_child = klass._execute_child
                def _execute_child(*args):

                    (self, args, executable, preexec_fn, close_fds,
                                   cwd, env, universal_newlines,
                                   startupinfo, creationflags, shell, to_close,
                                   p2cread, p2cwrite,
                                   c2pread, c2pwrite,
                                   errread, errwrite) = _unpack_args(args)

                    if preexec_fn:
                        return wrapped_execute_child(self, args, executable, preexec_fn, close_fds,
                                       cwd, env, universal_newlines,
                                       startupinfo, creationflags, shell,
                                       p2cread, p2cwrite,
                                       c2pread, c2pwrite,
                                       errread, errwrite)

                    for fd in (p2cread, p2cwrite,
                                       c2pread, c2pwrite,
                                       errread, errwrite):
                        if fd is not None:
                            _set_cloexec_flag(fd, False)

                    errpipe_read, errpipe_write = os.pipe()

                    data = base64.encodestring(
                            pickle.dumps(
                                dict(
                                    args=args, executable=executable, close_fds=close_fds,
                                    cwd=cwd, env=env, shell=shell,
                                    p2cread=p2cread, p2cwrite=p2cwrite,
                                    c2pread=c2pread, c2pwrite=c2pwrite,
                                    errread=errread, errwrite=errwrite,
                                    errpipe_read=errpipe_read, errpipe_write=errpipe_write,
                                ), pickle.HIGHEST_PROTOCOL))

                    use_file = len(data) >= ARG_MAX

                    if use_file:
                        with tempfile.NamedTemporaryFile(delete=False) as the_file:
                            the_file.write(data)
                        argv = (ctypes.c_char_p * 5)(sys.executable, __file__,
                                '@', the_file.name, 0)
                    else:
                        argv = (ctypes.c_char_p * 4)(sys.executable, __file__, data, 0)

                    pid = ctypes.c_int()

                    os_environ = (ctypes.c_char_p * (len(os.environ)+1))(
                            *(['{0}={1}'.format(*value) for value in os.environ.iteritems()]+[0]))

                    try:
                        ret = posix_spawn(ctypes.byref(pid), ctypes.c_char_p(sys.executable),
                                ctypes.c_void_p(), ctypes.c_void_p(),
                                ctypes.cast(argv, ctypes.POINTER(ctypes.c_char_p)),
                                ctypes.cast(os_environ, ctypes.POINTER(ctypes.c_char_p)))
                        err = ctypes.get_errno()
                        os.close(errpipe_write)
                        if ret:
                            raise OSError(err, os.strerror(err))
                        self.pid = pid.value
                        self._child_created = True
                        # Wait for exec to fail or succeed; possibly raising exception
                        # Exception limited to 1M
                        data = _eintr_retry_call(os.read, errpipe_read, 1048576)
                        if data:
                            try:
                                _eintr_retry_call(os.waitpid, self.pid, 0)
                            except OSError as e:
                                if e.errno != errno.ECHILD:
                                    raise
                            raise pickle.loads(data)
                    finally:
                        if use_file:
                            try:
                                os.unlink(the_file.name)
                            except:
                                pass
                        os.close(errpipe_read)
                        if p2cread is not None and p2cwrite is not None:
                            _close_in_parent(p2cread, to_close)
                        if c2pwrite is not None and c2pread is not None:
                            _close_in_parent(c2pwrite, to_close)
                        if errwrite is not None and errread is not None:
                            _close_in_parent(errwrite, to_close)

                klass._execute_child = _execute_child


            import subprocess
            _wrap_execute_child(subprocess.Popen)

# vim: set et ts=4 sw=4 ai :

