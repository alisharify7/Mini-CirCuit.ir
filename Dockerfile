FROM python:alpine

LABEL maintainer="alisharifyofficial@gmail.com"

RUN mkdir /usr/src/app

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN apk update

RUN pip3 install -r /usr/src/app/dev-requirements.txt
RUN pip3 install gunicorn
# RUN flask db init

# CMD flask db migrate
# CMD flask db upgrade
EXPOSE 8000
CMD gunicorn -w 4 -b 0.0.0.0:8000 app:app

