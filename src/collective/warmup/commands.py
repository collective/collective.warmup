import logging
from .checker import Checker


def warmup(configuration):
    checker = Checker(configuration)

    if not checker.enabled:
        exit(0)

    checker.execute()
