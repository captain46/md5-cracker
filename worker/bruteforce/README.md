# Bruteforce Worker
This is the third instance in the chain of MD5 password-cracking workers.

## Functionality
The bruteforce worker tries to... well... bruteforce a collision for the received hash. This make take a very long time. 
If a collision is found a response message with routing key `found` is send to the configured exchange.
Otherwise the routing key `md5.bruteforce` is used.

## Configuration
The worker can be configured with the provided `config.ini`.

## Requirements
The worker requires Python3 with the following modules
- redis `pip install redis`
- pika `pip install pika`