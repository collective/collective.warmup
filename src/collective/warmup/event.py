import logging
import os
import subprocess
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
            proc = subprocess.Popen(
                [
                    "%s %s -p %d" % (
                        warmup_bin, warmup_ini, zserver.port
                    )
                ],
                shell=True
            )
