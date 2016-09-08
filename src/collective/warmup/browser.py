""" Browser views
"""
import logging
from Products.Five.browser import BrowserView
from collective.warmup.config import WARMUP, HEALTH_THRESHOLD
logger = logging.getLogger('collective.warmup')


class HealthCheck(BrowserView):
    """ Health check view to be used with load-balancers health check.
    """

    @property
    def threshold(self):
        """ Health threshold
        """
        return HEALTH_THRESHOLD

    @property
    def cacheSize(self):
        """ Current DB cache size
        """
        return self.context._p_jar.db().cacheSize()

    @property
    def healthy(self):
        """ Is Zope instance healthy
        """
        if WARMUP['done']:
            logger.debug("Healthy forever")
            return True

        if self.cacheSize >= self.threshold:
            logger.info("HEALTHY - db cache size %s/%s", self.cacheSize, self.threshold)
            WARMUP['done'] = True
        return WARMUP['done']
        
    def __call__(self, *args, **kwargs):
        if self.healthy:
            return 'ok'

        msg = "UNHEALTHY - db cache size too low: %s/%s" % (self.cacheSize, self.threshold)
        logger.warn(msg)
        self.request.response.setStatus(503, msg)
        return msg
