FROM rabbitmq:management
MAINTAINER Richard Raumberger <richard.raumberger@fh-joanneum.at>

RUN apt-get update && apt-get install -y curl && apt-get autoremove && apt-get clean

WORKDIR /app
ADD init.sh rabbitmq-configuration.json /app/

RUN chmod 0777 /app/*

CMD ["/app/init.sh"]

