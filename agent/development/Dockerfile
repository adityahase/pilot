FROM python:3.13

ENV PYTHONUNBUFFERED=1

RUN apt update && apt install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://code-server.dev/install.sh | sh && \
    code-server --install-extension ms-python.python && \
    code-server --install-extension charliermarsh.ruff

RUN pip install honcho

COPY . /agent
RUN --mount=type=cache,target=/root/.cache/pip pip install -e /agent

RUN echo 1
RUN mkdir -p /root/.local/share/code-server/User && \
    cp /agent/development/settings.json /root/.local/share/code-server/User/settings.json && \
    rm /agent/.vscode/settings.json
WORKDIR /agent
ENTRYPOINT [ "honcho" ]
CMD ["-f", "development/Procfile", "start"]