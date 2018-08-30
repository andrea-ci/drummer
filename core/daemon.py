#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os, time, atexit

"""
Daemon base

This file contains the daemon base class for a UNIX daemon.
"""

class Daemon:
    """A generic daemon base class.

    Usage: subclass this class and override the run() method.
    """

    def __init__(self, pidfile, workpath='/'):
        """Constructor.

        We need the pidfile for the atexit cleanup method.
        The workpath is the path the daemon will operate
        in. Normally this is the root directory, but can be some
        data directory too, just make sure it exists.
        """
        self.pidfile = pidfile
        self.workpath = workpath


    def perror(self, msg, err):
        """Print error message and exit. (helper method)
        """
        msg = msg + '\n'
        sys.stderr.write(msg.format(err))
        sys.exit(1)


    def daemonize(self):
        """Deamonize class process. (UNIX double fork mechanism).
        """

        if not os.path.isdir(self.workpath):
            self.perror('workpath does not exist!', '')

        # fork #1
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent process
                sys.exit(0)

        except OSError as err:
            self.perror('fork #1 failed: {0}', err)

        # decouple from parent environment
        try:
            os.chdir(self.workpath)

        except OSError as err:
            self.perror('path change failed: {0}', err)

        os.setsid()
        os.umask(0)

        # exit from second parent
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)

        except OSError as err:
            self.perror('fork #2 failed: {0}', err)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(os.remove, self.pidfile)
        pid = str(os.getpid())
        with open(self.pidfile,'w+') as f:
            f.write(pid + '\n')
        self.run()


    def run(self):
        """Worker method.

        It will be called after the process has been daemonized
        by start() or restart(). You'll have to overwrite this
        method with the daemon program logic.
        """
        while True:
            time.sleep(1)
