""" Browser views
"""
import os
import logging
from Products.Five.browser import BrowserView

logger = logging.getLogger('collective.warmup')

HEALTH_THRESHOLD = os.environ.get('WARMUP_HEALTH_THRESHOLD', None)
if HEALTH_THRESHOLD is None:
    logger.warn("DISABLED @@health.check: WARMUP_HEALTH_THRESHOLD env not set")
else:
    logger.warn("ENABLED @@health.check: WARMUP_HEALTH_THRESHOLD = %s",
                HEALTH_THRESHOLD)

class HealthCheck(BrowserView):
    """ Health check view to be used with load-balancers health check.
    """
    def __call__(self, *args, **kwargs):
        if HEALTH_THRESHOLD is None:
            return "ok"

        try:
            threshold = int(HEALTH_THRESHOLD)
            cacheSize = self.context._p_jar.db().cacheSize()
        except Exception, err:
            logger.exception(err)
            return "ok"
        else:
            if cacheSize < threshold:
                msg = "DB cache size to low: %s/%s" % (cacheSize, threshold)
                logger.warn(msg)
                self.request.response.setStatus(503, msg)
                return msg
            return 'ok'
