FROM redis:alpine
MAINTAINER Richard Raumberger <richard.raumberger@fh-joanneum.at>

RUN mkdir /etc/redis
RUN echo "requirepass secured" > /etc/redis/redis.conf

CMD [ "redis-server", "/etc/redis/redis.conf" ]