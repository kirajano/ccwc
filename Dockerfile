FROM python:3.8.12-slim-buster

    # Python
ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # uv version 0.5.24
    UV_PACKAGE_MANAGER_GIT="git+https://github.com/astral-sh/uv.git@42fae925c44b99aebbda09d0a2ed7659ce7b8e15" \
    # Do not use venv but docker python
    UV_SYSTEM_PYTHON=1

RUN apt-get update \
    && pip install --upgrade pip \
    && pip install $UV_PACKAGE_MANAGER_GIT \
    && apt-get clean

WORKDIR /wc_tool
COPY ./ccwc/*.py ./ccwc/
COPY ./tests/*.py ./tests/
COPY pyproject.toml .

COPY uv.lock .
RUN uv sync --no-editable \
    && uv build --wheel \
    && uv pip install dist/*.whl

CMD ["bash"]


