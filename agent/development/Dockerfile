FROM python:3.13

ENV PYTHONUNBUFFERED=1

RUN apt update && apt install -y --no-install-recommends \
    curl \
    ca-certificates \
    tmux \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://code-server.dev/install.sh | sh && \
    code-server --install-extension ms-python.python && \
    code-server --install-extension charliermarsh.ruff

RUN wget https://github.com/DarthSim/overmind/releases/download/v2.5.1/overmind-v2.5.1-linux-amd64.gz && \
    gunzip -d overmind-v2.5.1-linux-amd64.gz && \
    mv overmind-v2.5.1-linux-amd64 /usr/local/bin/overmind && \
    chmod +x /usr/local/bin/overmind

COPY . /agent
RUN --mount=type=cache,target=/root/.cache/pip pip install -e /agent

RUN echo 1
RUN mkdir -p /root/.local/share/code-server/User && \
    cp /agent/development/settings.json /root/.local/share/code-server/User/settings.json && \
    rm /agent/.vscode/settings.json
WORKDIR /agent
ENTRYPOINT [ "overmind" ]
CMD ["start", "-f", "development/Procfile", "--no-port", "-c", "web", "-r", "web"]