FROM ubuntu:latest

RUN apt-get update -y && apt-get install -y locales python3-pip python3-dev

WORKDIR /app

COPY /app/requirements.txt ./
COPY /app/.env ./
COPY /app/templates ./templates
COPY /app/static ./static


RUN pip3 install -r requirements.txt

COPY /app ./

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

EXPOSE 8080
CMD [ "python3", "run.py" ]