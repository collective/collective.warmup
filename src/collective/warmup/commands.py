import argparse
from .checker import Checker


def warmup(configuration):

    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="zope instance port")
    params = parser.parse_args()

    checker = Checker(configuration, params.port)

    if not checker.enabled:
        exit(0)

    checker.execute()
