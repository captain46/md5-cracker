/**
 * Created by raphaelhartner on 7/5/16.
 */
var amqp = require('amqplib/callback_api');
var exchange = 'password-cracker';

function start(){

    var data = {
        'hash':'912ec803b2ce49e4a541068d495ab570',
        'type':'MD5',
        'origin':'password-worker.MD5.database',
        'password':'not the correct password'
    }

    amqp.connect('amqp://distcomp-md5-cracker:distcomp@localhost', function(err, conn) {

        if(err){
            console.log(err);
            return;
        }else {

            conn.createChannel(function (err, ch) {

                ch.assertExchange(exchange, 'direct', {durable: false});
                ch.publish(exchange, 'found', new Buffer(JSON.stringify(data)));
                console.log('send msg to exchange!');

            });

            setTimeout(function () {
                conn.close();
                process.exit(0)
            }, 5000);
        }
    });

}

start();