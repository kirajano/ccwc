
########
# BASE #
########
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

ENV APP="ccwc" \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    UV_SYSTEM_PYTHON=1 

RUN apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

WORKDIR /wc_tool


########
# DEV #
########
FROM base AS dev

RUN uv init --app $APP

ARG USERNAME=developer
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && chown -R $USERNAME:$USERNAME /wc_tool

USER $USERNAME
ENV SHELL /bin/bash

########
# BUILD #
########
FROM base AS build

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

# Run tests
RUN pytest tests


########
# PROD #
########
FROM build as prod

ENTRYPOINT [ "ccwc" ]
CMD [ "-c", "tests/test.txt" ]


