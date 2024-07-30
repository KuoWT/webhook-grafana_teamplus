FROM python:3.9-slim

WORKDIR /code

ADD . /code

RUN pip install -r requirements.txt

CMD ["python", "guardian-grafana.py"]
