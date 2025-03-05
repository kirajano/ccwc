"""
Enables the folder to be a python package
"""

__app_name__ = "ccwc"
__version__ = "0.1.0"

(
    SUCCESS,
    STDIN_ERROR,
    FILE_ERROR,
) = range(3)

ERRORS = {
    STDIN_ERROR: "standard input error encountered",
    FILE_ERROR: "file error encountered - please check path",
}
