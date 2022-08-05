FROM python:3.8-alpine
MAINTAINER Aleksey Golikov 'golikov.aleksey.1987@yandex.ru'
WORKDIR /home/app
COPY . /home/app
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "app.py"]