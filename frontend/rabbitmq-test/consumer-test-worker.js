/**
 * Created by raphaelhartner on 7/5/16.
 */

var amqp = require('amqplib/callback_api');
var exchange = 'password-cracker';

function start(){

    amqp.connect('amqp://distcomp-md5-cracker:distcomp@localhost', function(err, conn) {
        conn.createChannel(function(err, ch) {
            ch.assertExchange(exchange, 'direct', {durable: false});

            ch.assertQueue('password-cracker.response', {durable:true}, function(err, q){

                if(err){
                    console.log(err);
                    return;
                }

                ch.consume(q.queue, function(msg){
                    console.log(msg.content.toString());
                }, {noAck: true});

            });
        });

        setTimeout(function() { conn.close(); process.exit(0) }, 100000);
    });
}

start();