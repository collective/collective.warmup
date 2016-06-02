""" Various configuration
"""
import os
import logging
logger = logging.getLogger('collective.warmup')

HEALTH_THRESHOLD = os.environ.get('WARMUP_HEALTH_THRESHOLD', None)
WARMUP = {'done': False}

if HEALTH_THRESHOLD is None:
    logger.warn("DISABLED @@health.check: WARMUP_HEALTH_THRESHOLD env not set")
    WARMUP['done'] = True
else:
    try:
        HEALTH_THRESHOLD = int(HEALTH_THRESHOLD)
    except Exception, err:
        logger.exception(err)
        logger.warn("DISABLED @@health.check: See error above for details")
        WARMUP['done'] = True
    else:
         logger.warn("ENABLED @@health.check: WARMUP_HEALTH_THRESHOLD = %s", HEALTH_THRESHOLD)
