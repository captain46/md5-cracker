FROM alpine:latest
MAINTAINER Richard Raumberger <richard.raumberger@fh-joanneum.at>

RUN apk update && apk add python3 py-pip && rm -r /var/cache/

WORKDIR /app
ADD . /app/

RUN python3 -m pip install pika redis

RUN sed -i '5s/host.*=.*localhost/host = broker/g' /app/config.ini
RUN sed -i '13s/host.*=.*localhost/host = redis/g' /app/config.ini
RUN sed -i '15s/password =/password = secured/g' /app/config.ini

ENTRYPOINT sleep 10 && python3 worker.py