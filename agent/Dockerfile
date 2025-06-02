FROM python:3.13-slim

COPY . /agent
RUN --mount=type=cache,target=/root/.cache/pip pip install /agent

WORKDIR /agent

ENV PYTHONUNBUFFERED=1

ENTRYPOINT [ "hypercorn" ]
CMD [ "--bind", "0.0.0.0:8000", "agent.web:app" ]