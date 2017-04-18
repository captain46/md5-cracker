# Rainbow-Table Worker
This is the second instance in the chain of MD5 password-cracking workers.

## Functionality
The rainbow-table worker looks up the MD5 hash value in the configured rainbow-table file.
If the rainbow-table contains the hash a response message with routing key `found` is send to the configured exchange.
Otherwise the routing key `md5.rainbow` is used.

## Configuration
The worker can be configured with the provided `config.ini`.

## Requirements
The worker requires Python3 with the following modules
- redis `pip install redis`
- pika `pip install pika`