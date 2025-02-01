"""
Enables to run `python -m ccwc` as entrypoint
"""
from ccwc import cli, __app_name__


if __name__ == '__main__':
    cli.app(prog_name=__app_name__)
    