"""
Enables to run `python -m ccwc` as entrypoint
"""
from ccwc import __app_name__, cli

if __name__ == '__main__':
    cli.app(prog_name=__app_name__)
