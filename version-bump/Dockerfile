FROM python:3-alpine

ADD . /app

WORKDIR /app

RUN pip3 install lxml --target=/app

ENV PYTHONPATH /app

CMD ["/app/main.py"]
ENTRYPOINT ["python", "-u"]
