#!/usr/bin/env python3
# Author: Richard Raumberger

import pika
import json
import redis
import configparser
import hashlib

config = configparser.ConfigParser()
config.read('config.ini')

WORKER_TYPE = config['worker']['type']
WORKER_MAXIMAL_PASSWORD_LENGTH = int(config['worker']['maxLength'])

BROKER_HOST = config['broker']['host']
BROKER_PORT = int(config['broker']['port'])
BROKER_USER = config['broker']['user']
BROKER_PASSWORD = config['broker']['password']
RECV_QUEUE_NAME = config['broker']['recvQueue']
EXCHANGE_NAME = config['broker']['exchange']

REDIS_HOST = config['redis']['host']
REDIS_PORT = int(config['redis']['port'])
REDIS_PASSWORD = config['redis']['password']


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

    collided_password = find_hash_collision(md5)
    if collided_password is not None:
        print("Password for '{}' is '{}'".format(
            md5,
            collided_password
        ))

        message['password'] = collided_password
        routing_key = 'found'

        print('Storing {}:{} in redis'.format(md5, collided_password))
        redis_connection.set(md5, collided_password)
    else:
        print(
            "No password found in redis for '{}'. Returning message...".format(
                md5
            ))
        routing_key = message['type'] + '.' + WORKER_TYPE

    message['origin'] = WORKER_TYPE
    publish(channel, routing_key, message)


#########################################################################################################
# Based on an version provided by Thomas Klampfl                                                        #
#########################################################################################################


def find_hash_collision(password_hash):
    for baseWidth in range(1, WORKER_MAXIMAL_PASSWORD_LENGTH):
        print("Checking passwords for {} with length: {}".format(password_hash, baseWidth))
        password = recursive_check(baseWidth, 0, "", password_hash)
        if password is not None:
            return password
    return None


def recursive_check(width, position, base_string, password_hash):
    for char in range(32, 127):
        if position < width - 1:
            collided_password = recursive_check(width, position + 1, base_string + "%c" % char, password_hash)
            if collided_password is not None:
                return collided_password
        collided_password = check_collision(password_hash, base_string + "%c" % char)
        if collided_password is not None:
            return collided_password
    return None


def check_collision(password_hash, possible_collision):
    md5_hash = hashlib.md5(possible_collision.encode('UTF-8')).hexdigest()
    if md5_hash.lower() == password_hash.lower():
        return possible_collision
    return None


#########################################################################################################

if __name__ == "__main__":
    main()
