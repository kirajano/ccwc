from ccwc import cli
from typer.testing import CliRunner


runner = CliRunner()

test_file = "tests/test.txt"

args_and_results = {
    "-c": str(342190),
    "-l": str(7145),
    "-w": str(58164),
    "-m": str(339292),
}


def test_byte_counter():
    result = runner.invoke(cli.app, ["-c", test_file])
    expected_result = args_and_results.get("-c")
    assert f"{expected_result} {test_file}" in result.stdout


def test_line_counter():
    result = runner.invoke(cli.app, ["-l", test_file])
    expected_result = args_and_results.get("-l")
    assert f"{expected_result} {test_file}" in result.stdout


def test_word_counter():
    result = runner.invoke(cli.app, ["-w", test_file])
    expected_result = args_and_results.get("-w")
    assert f"{expected_result} {test_file}" in result.stdout


def test_char_counter():
    result = runner.invoke(cli.app, ["-m", test_file])
    expected_result = args_and_results.get("-m")
    assert f"{expected_result} {test_file}" in result.stdout