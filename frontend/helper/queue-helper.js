/**
 * Created by raphaelhartner on 7/5/16.
 */
var amqp = require('amqplib/callback_api');
var config = require('../config/config');
var exchange = 'password-cracker';
var channel;

module.exports.establishChannelConnections = function (callback) {

    amqp.connect('amqp://' + config.BROKER_USER + '@' + config.BROKER_HOST, function (err, conn) {
        if (err) {
            console.log(err);
            process.exit(1);
        }
        conn.createChannel(function (err, ch) {
            if (err) {
                console.log(err);
                process.exit(1);
            }
            ch.assertExchange(exchange, 'direct', {durable: false});
            channel = ch;
            console.log('established channel!');
            callback();
        });
    });

};

module.exports.bindToResponseQueue = function (callback) {

    channel.assertQueue('password-cracker.response', {durable: true}, function (err, q) {

        channel.consume(q.queue, function (msg) {

            var data = JSON.parse(msg.content);
            console.log("received password '" + data.password + "' for hash '" + data.hash + "'");
            callback(data);

        }, {noAck: true});

    });

};

/**
 *
 * @param data must have properties for 'hash', 'type'
 *          'origin' will be added before sending
 */

module.exports.sendHashRequest = function (data) {
    data.origin = 'frontend';
    var routingKey = (data.type && data.type.toUpperCase()) + '.frontend';
    console.log("routing-key for '" + data.hash + "' is '" + routingKey + "'");

    channel.publish(exchange, routingKey, new Buffer(JSON.stringify(data)));
};

