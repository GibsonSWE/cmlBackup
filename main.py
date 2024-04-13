from src import constants as c
from src import utils
from src import cml_api as cml

import sys


def cml():
    labs = cml.get_labs()

    for lab in labs:
        pass


def main():
    if '--version' in sys.argv or '-v' in sys.argv:
        print(utils.show_version())

    if '--help' in sys.argv or '-h' in sys.argv:
        print(utils.show_help())


if __name__ == "__main__":
    main()
