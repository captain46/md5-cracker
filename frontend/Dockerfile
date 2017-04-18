FROM irakli/node-alpine:6.2-runit
MAINTAINER Richard Raumberger <richard.raumberger@fh-joanneum.at>

WORKDIR /app
ADD . /app/

RUN npm install
RUN sed -i 's/localhost/broker/g' /app/config/config.js

ENTRYPOINT sleep 10 && node frontend-server.js