"""
Module for Application CLI
"""

from typing import Optional
import typer
from ccwc import __app_name__, __version__, ERRORS
from ccwc.counters import (
    ContentCounter,
    FileByteCounter, 
    FileLineCounter, 
    FileWordCounter,
    FileCharCounter,
    StdInByteCounter,
    StdInLineCounter,
    StdInWordCounter,
    StdInCharCounter
)
from typing import Optional
import sys


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"Application: {__app_name__}: v{__version__}")
        raise typer.Exit()


def _display_content_count(content_counter: ContentCounter) -> int:
    """
    Helper function for displaying erorrs if encountered
    """
    counter = content_counter.count_content()

    error_code = counter.error_code

    if error_code in ERRORS.keys():
        typer.secho(f"{ERRORS.get(error_code)}", fg=typer.colors.BRIGHT_RED)
        sys.exit(error_code)
    
    return counter.content_length


def _count_bytes(file_path: Optional[str]) -> int:
    """
    Count bytes for file or standard input and return length
    """
    if file_path:
        content_counter = FileByteCounter(file_path)
    else:
        content_counter = StdInByteCounter()

    content_length = _display_content_count(content_counter)
    
    return content_length


def _count_lines(file_path: Optional[str]) -> int:
    """
    Count lines in file for file or standard input and return length
    """
    if file_path:
        content_counter = FileLineCounter(file_path) 
    else:
        content_counter = StdInLineCounter()

    content_length = _display_content_count(content_counter)
    
    return content_length


def _count_words(file_path: Optional[str]) -> None:
    if file_path:
        content_counter = FileWordCounter(file_path)
    else:
        content_counter = StdInWordCounter()

    content_length = _display_content_count(content_counter)

    return content_length


def _count_chars(file_path: Optional[str]) -> None:
    if file_path:
        content_counter = FileCharCounter(file_path)
    else:
        content_counter = StdInCharCounter()

    content_length = _display_content_count(content_counter)

    return content_length


app = typer.Typer(
    help="CCWC from https://codingchallenges.fyi/ application mimics the `wc` standard command line tool in Linux",
    no_args_is_help=True,
)


@app.callback(invoke_without_command=True)
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Display the applications version and exit",
        callback=_version_callback,
        is_eager=True,
    ),
    file_path: str = typer.Argument(
        None,
        help="Path to the file to process",
    ),
    count_bytes: bool = typer.Option(
        False,
        "-c",
        help="Count bytes in file input or standard input",
    ),
    count_file_lines: bool = typer.Option(
        False,
        "-l",
        help="Count lines in file input",
    ),
    count_file_words: bool = typer.Option(
        False,
        "-w",
        help="Count words in file input",
    ),
    count_file_chars: bool = typer.Option(
        False,
        "-m",
        help="Count characters in file input considering locale"
    ),
) -> None:
    all_args = [
        count_bytes, 
        count_file_lines,
        count_file_words,
        count_file_chars
        ]
    
    if not any (all_args):
        bytes_count = _count_bytes(file_path)
        lines_count = _count_lines(file_path)
        words_count = _count_words(file_path)
        typer.echo(f"{lines_count} {words_count} {bytes_count} {file_path}")
    else:
        if count_bytes:
            content_length = _count_bytes(file_path)
            if file_path:
                typer.secho(f"{content_length} {file_path}", fg=typer.colors.BRIGHT_CYAN)
            else:
                typer.secho(f"{content_length}", fg=typer.colors.CYAN)
        if count_file_lines:
            content_length = _count_lines(file_path)
            if file_path:
                typer.secho(f"{content_length} {file_path}", fg=typer.colors.BRIGHT_BLACK)
            else:
                typer.secho(f"{content_length}", fg=typer.colors.BLACK)
        if count_file_words:
            content_length = _count_words(file_path)
            if file_path:
                typer.secho(f"{content_length} {file_path}", fg=typer.colors.BRIGHT_BLUE)
            else:
                typer.secho(f"{content_length}", fg=typer.colors.BLUE)
        if count_file_chars:
            content_length = _count_chars(file_path)
            if file_path:
                typer.secho(f"{content_length} {file_path}", fg=typer.colors.BRIGHT_YELLOW)
            else:
                typer.secho(f"{content_length}", fg=typer.colors.YELLOW)
    raise typer.Exit()
