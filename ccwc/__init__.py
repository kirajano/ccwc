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

"""
NEXT TO DOS TO FINALIZE
    
    

    Notes:
    uv init
    source .venv/bin/activate
    uv add -r requirements.txt
    uv tree
    uv run -m ccwc -c tests/test.txt --> run as a module
    pip install -e . --> to install in development mode

    uv build --> if you want to publish

    0. For some reason, the uv virtual environment makes the installation globall and classic venv not...Find out why and define best practice. 
    1. Check when installing if isolated or docker is already needed?
    2. See how to run installed package in uv
    2. Decide if build is neded

-Docker: multi-layer like Ludwig or devcontainer for better IDE integration
- Short Readme and publish to GH
- Maybe very basic CICD
"""