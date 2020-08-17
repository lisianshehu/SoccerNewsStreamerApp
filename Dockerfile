FROM python:3

WORKDIR /app

COPY /app/requirements.txt ./
COPY /app/templates ./templates
COPY /app/static ./static

RUN pip install -r requirements.txt

COPY /app ./

EXPOSE 8080
CMD [ "python", "run.py" ]