FROM python:3.10-alpine

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]