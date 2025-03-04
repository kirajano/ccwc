from typer.testing import CliRunner

from ccwc import cli

runner = CliRunner()

args_and_results = {
    "-c": str(12),
    "-l": str(2),
    "-w": str(2),
    "-m": str(12),
}


def test_byte_counter():
    result = runner.invoke(cli.app, args=["-c"], input="""Hello World!""")
    expected_result = args_and_results.get("-c")
    assert f"{expected_result}" in result.stdout


def test_line_counter():
    result = runner.invoke(cli.app, args=["-l"], input="""Hello \n World!""")
    expected_result = args_and_results.get("-l")
    assert f"{expected_result}" in result.stdout


def test_word_counter():
    result = runner.invoke(cli.app, args=["-w"], input="""Hello World!""")
    expected_result = args_and_results.get("-w")
    assert f"{expected_result}" in result.stdout


def test_char_counter():
    result = runner.invoke(cli.app, args=["-m"], input="""Hello World!""")
    expected_result = args_and_results.get("-m")
    assert f"{expected_result}" in result.stdout
