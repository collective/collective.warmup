from App.config import getConfiguration
import logging
import subprocess
import time
from ZServer.HTTPServer import zhttp_server


logger = logging.getLogger('WARMUP ::: ')


class Starting(object):

    def __init__(self, event):
        logger.warning('Starting Warmup')

        config = getConfiguration()
        config.servers
        zserver = [
            server for server in config.servers
            if isinstance(server, zhttp_server)
        ][0]
        subprocess.Popen(["bin/warmup", str(zserver.port)]).pid
