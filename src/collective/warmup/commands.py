import argparse
from collective.warmup.checker import Checker


def warmup():

    parser = argparse.ArgumentParser()
    parser.add_argument("configuration_file", help="Warmup configuration file")
    parser.add_argument(
        "--port", '-p', default="80",
        type=int, help="zope instance port"
    )
    params = parser.parse_args()

    checker = Checker(params.configuration_file, params.port)

    if not checker.enabled:
        exit(0)

    checker.execute()
