import logging
import ConfigParser as configparser

logging.basicConfig()

logger = logging.getLogger('Collective Warmup')
logger.setLevel(logging.INFO)


def warmup(configuration):
    logger.info(configuration)
    config = configparser.ConfigParser({'enabled': 'True'})
    config.read(configuration)

    enabled = config.getboolean('warmup', 'enabled')
    if not enabled:
        logger.info('Warmup script has been disabled')
        exit(0)
    import pdb; pdb.set_trace( )
