# This shell script is based upon an idea from
# http://stackoverflow.com/questions/31403873/import-broker-definitions-into-dockerized-rabbitmq
sleep 7 && curl -i -u guest:guest -d @/app/rabbitmq-configuration.json -H "content-type:application/json" http://localhost:15672/api/definitions -X POST &

rabbitmq-server $@