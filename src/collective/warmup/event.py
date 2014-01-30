import logging
import os
import subprocess
import time
from App.config import getConfiguration
from ZServer.HTTPServer import zhttp_server


logger = logging.getLogger('WARMUP ::: ')


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
        if not warmup_bin:
            logger.error('WARMUP_BIN not set')
        else:
            logger.info('Starting Warmup')
            proc = subprocess.Popen(
                ["{0} {1}".format(warmup_bin, zserver.port)],
                shell=True
            )
