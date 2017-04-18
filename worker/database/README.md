# Database Worker
This is the first instance in the chain of MD5 password-cracking workers.

## Functionality
The database worker looks up the MD5 hash value in the configured redis instance.
If the hash contains a password in redis a response message with routing key `found` is send to the configured exchange.
Otherwise the routing key `md5.database` is used.

## Configuration
The worker can be configured with the provided `config.ini`.

## Requirements
The worker requires Python3 with the following modules
- redis `pip install redis`
- pika `pip install pika`