import logging
import os
import subprocess
import thread
import time
from App.config import getConfiguration
from ZServer.HTTPServer import zhttp_server


logger = logging.getLogger('Collective Warmup')


class Starting(object):

    def __init__(self, event):
        config = getConfiguration()
        config.servers
        zserver = [
            server for server in config.servers
            if isinstance(server, zhttp_server)
        ][0]
        time.sleep(5)

        warmup_bin = os.environ.get('WARMUP_BIN', False)
        warmup_ini = os.environ.get('WARMUP_INI', False)
        if not warmup_bin:
            logger.error('WARMUP_BIN not set')
        if not warmup_ini:
            logger.error('WARMUP_INI not set')

        if warmup_bin and warmup_ini:
            logger.info('Executing intances warmup')

            command = "%s %s -p %d" % (warmup_bin, warmup_ini, zserver.port)

            # Since the warmup subprocess waits for Zope to be finished starting
            # up and handling requests, we should not block the startup here.
            # But it is important to collect the result of the subprocess (by
            # using subprocess.check_call) in order to avoid zombie processes.
            # However, since subprocess.check_call is blocking the caller, we call
            # it within a new thread which will have the patience to wait for the
            # subprocess to finish and the main startup process can continue.
            thread.start_new_thread(subprocess.check_call,
                                    ([command],),
                                    {'shell': True})
