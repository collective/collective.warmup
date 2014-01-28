import logging
import time
import subprocess
import os


logger = logging.getLogger('WARMUP ::: ')


class Starting(object):
    """docstring for ClassName"""
    def __init__(self, event):
        logger.warning('Starting Warmup')
        # time.sleep(5)

        # from App.config import getConfiguration
        # config = getConfiguration()
        # import pdb; pdb.set_trace( )

        # XXX: get a real path
        # pid = subprocess.Popen(["bin/warmup.py"]).pid
        logger.warning('Warmup DONE!')
