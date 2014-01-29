from App.config import getConfiguration
import logging
import subprocess
import time
from ZServer.HTTPServer import zhttp_server


logger = logging.getLogger('WARMUP ::: ')


class Starting(object):
    """docstring for ClassName"""
    def __init__(self, event):
        logger.warning('Starting Warmup')
        # time.sleep(5)

        # config = getConfiguration()
        # import pdb; pdb.set_trace( )
        # config = getConfiguration()
        # zserver = [
        #     server for server in config.servers
        #     if isinstance(server, zhttp_server)
        # ][0]

        pid = subprocess.Popen(["bin/warmup"]).pid
