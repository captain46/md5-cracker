#!/usr/bin/env python3
# Author: Richard Raumberger

import pika
import json
import configparser
import redis

config = configparser.ConfigParser()
config.read('config.ini')

WORKER_TYPE = config['worker']['type']
RAINBOW_TABLE_PATH = config['worker']['rainbowTablePath']

BROKER_HOST = config['broker']['host']
BROKER_PORT = int(config['broker']['port'])
BROKER_USER = config['broker']['user']
BROKER_PASSWORD = config['broker']['password']
RECV_QUEUE_NAME = config['broker']['recvQueue']
EXCHANGE_NAME = config['broker']['exchange']

REDIS_HOST = config['redis']['host']
REDIS_PORT = int(config['redis']['port'])
REDIS_PASSWORD = config['redis']['password']


def build_rainbow_table(filename):
    table = dict()
    file = open(filename, 'r')

    for line in file.readlines():
        rainbow_entry = line.split(':')
        table[rainbow_entry[0]] = rainbow_entry[1].replace('\n', '')

    return table


RAINBOW_TABLE = build_rainbow_table(RAINBOW_TABLE_PATH)


def main():
    print('Initializing broker connction...')
    print('Broker-Parameters:\nHost: {}\nPort: {}\nUser: {}\nPassword: {}'.format(
        BROKER_HOST, BROKER_PORT, BROKER_USER, BROKER_PASSWORD))
    broker_config = pika.ConnectionParameters(BROKER_HOST, BROKER_PORT,
                                              credentials=pika.PlainCredentials(BROKER_USER, BROKER_PASSWORD))
    pika.SelectConnection(broker_config, on_connection_open, stop_ioloop_on_close=False).ioloop.start()


def on_connection_open(connection):
    print('Broker connection initialized')
    print('Opening broker channel')
    connection.channel(on_open_callback=on_channel_open)


def on_channel_open(channel):
    print('Broker channel opened')
    print('Initializing redis connction...')
    print('Redis-Parameters:\nHost: {}\nPort: {}\nPassword:{}'.format(
        REDIS_HOST, REDIS_PORT, REDIS_PASSWORD))
    redis_connection = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASSWORD)
    print('Redis connction initialized')

    channel.basic_consume(consume_message_callback(redis_connection, channel), queue=RECV_QUEUE_NAME, no_ack=True)
    print('''Waiting for messages in queue "{}" on "{}".'''.format(RECV_QUEUE_NAME, BROKER_HOST))


def consume_message_callback(redis_connection, channel):
    return lambda ch, method, properties, body: handle_message(body, redis_connection, channel)


def publish(channel, routing_key, message):
    channel.basic_publish(exchange=EXCHANGE_NAME,
                          routing_key=routing_key,
                          body=json.dumps(message),
                          properties=pika.BasicProperties(
                              delivery_mode=1,  # make message transient
                          ))


def handle_message(body, redis_connection, channel):
    message = json.loads(body.decode())

    md5 = message['hash'].lower()
    print("Trying to find password for: {}".format(
        md5
    ))

    found_rainbow_table_password = RAINBOW_TABLE.get(md5)
    if found_rainbow_table_password is not None:
        print("Password for '{}' is '{}'".format(
            md5,
            found_rainbow_table_password
        ))

        message['password'] = found_rainbow_table_password
        routing_key = 'found'

        print('Storing {}:{} in redis'.format(md5, found_rainbow_table_password))
        redis_connection.set(md5, found_rainbow_table_password)
    else:
        print(
            "No password found in rainbow table for '{}'. Returning message...".format(
                md5
            ))
        routing_key = message['type'] + '.' + WORKER_TYPE

    message['origin'] = WORKER_TYPE
    publish(channel, routing_key, message)


if __name__ == "__main__":
    main()
