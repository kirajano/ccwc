from ccwc import (
    __app_name__,
    __version__,
    cli
)
from typer.testing import CliRunner


runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert f"v{__version__}" in result.stdout


def test_app_name():
    result = runner.invoke(cli.app, ["--version"])
    assert f"Application: {__app_name__}" in result.stdout