# syntax=docker/dockerfile:1

FROM python:3.8
EXPOSE 5000

RUN apt-get update
RUN yes | apt-get install python3-dev
RUN yes | apt-get install jq
RUN yes | apt-get install tzdata


COPY mosek.lic ./root/mosek/

COPY backend /backend 
WORKDIR /backend
RUN pip install -U pip
RUN pip install -r requirements.txt

RUN pip install Mosek

CMD ["uwsgi", "app.ini"]
