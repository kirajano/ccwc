
########
# BASE #
########
# uv official image
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

ENV APP="ccwc" \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Do not use venv but docker python
    UV_SYSTEM_PYTHON=1 

RUN apt-get update \
    # apt-get install <pckg1> <pckg2> \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

WORKDIR /wc_tool


########
# DEV #
########
FROM base AS dev

# Initiate project with uv (no need for `uv venv`)
RUN uv init $APP

# < Adding packages during development >
#     1. uv add <package==xx.yy.xx>
#     2. uv lock (after done)

# < Start and develop >
# uv run -m <module_name -flags args>

ENTRYPOINT [ "bash" ]

########
# BUILD #
########
FROM base AS build

# < Development Result >
# py
COPY ./ccwc/*.py ./ccwc/
COPY ./tests/*.py ./tests/
COPY ./tests/test.txt ./tests/test.txt
# toml
COPY pyproject.toml .

# Build app
COPY uv.lock .
RUN uv sync --no-editable
RUN uv build --wheel \
    && uv pip install dist/*.whl \
    && rm -r dist build ccwc.egg-info

########
# PROD #
########
FROM build as prod

ENTRYPOINT [ "ccwc" ]
CMD [ "-c", "tests/test.txt" ]


