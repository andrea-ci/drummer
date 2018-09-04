#!/usr/bin/python3
# -*- coding: utf-8 -*-
from core.configuration import Configuration
import sys, os, time, signal

class DaemonCtl:
    """ Control class for a daemon

    Usage:
    >>>    dc = DaemonCtl(daemon_base, '/tmp/foo.pid')
    >>>    dc.start()

    This class is the control wrapper for the above (daemon_base)
    class. It adds start/stop/restart functionality for it withouth
    creating a new daemon every time.
    """

    def __init__(self, Daemon, workdir='/'):
        """Constructor.

        @param daemon: daemon class (not instance)
        @param pidfile: daemon pid file
        @param workdir: daemon working directory
        """

        configuration = Configuration.load()
        daemon_config = configuration.get('daemon')

        self.Daemon = Daemon
        self.pidfile = daemon_config.get('pidfile')
        self.workdir = daemon_config.get('workdir')


    def start(self):
        """Start the daemon """

        # check for pidfile to see if the daemon already runs
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if pid:
            message = "pidfile {0} already exist. " + \
                    "Daemon already running?\n"
            sys.stderr.write(message.format(self.pidfile))
            sys.exit(1)

        # Start the daemon
        d = self.Daemon(self.pidfile, self.workdir)
        d.daemonize()


    def stop(self):
        """ Stop the daemon

        This is purely based on the pidfile / process control
        and does not reference the daemon class directly.
        """

        # get the pid from the pidfile
        try:
            with open(self.pidfile,'r') as pf:
                pid = int(pf.read().strip())

        except IOError: pid = None

        if not pid:
            message = "pidfile {0} does not exist. " + \
                    "Daemon not running?\n"
            # not an error in a restart
            sys.stderr.write(message.format(self.pidfile))

        else:

            # try killing the daemon process
            try:
                while True:
                    os.kill(pid, signal.SIGTERM)
                    time.sleep(0.1)

            except OSError as err:
                e = str(err.args)
                if e.find("No such process") > 0:
                    if os.path.exists(self.pidfile):
                        os.remove(self.pidfile)
                else:
                    print (str(err.args))
                    sys.exit(1)


    def restart(self):
        """Restart the daemon """

        self.stop()
        self.start()
