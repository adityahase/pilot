FROM python:3.13-slim

COPY . /agent
RUN pip install /agent

WORKDIR /agent

ENTRYPOINT [ "hypercorn" ]
CMD [ "--bind", "0.0.0.0:8000", "agent.web:app" ]