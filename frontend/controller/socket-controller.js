/**
 * Created by raphaelhartner on 7/4/16.
 */
"use strict";

var queueHelper = require('../helper/queue-helper.js');


module.exports.start = function (http) {

    var io = require('socket.io')(http);

    //all connected clients
    var clients = {};

    //dictionary of {hash:socketId}
    var requestedHashes = {};

    queueHelper.establishChannelConnections(webSocketHandler);

    function webSocketHandler() {

        queueHelper.bindToResponseQueue(handleWorkerResponse);

        io.on('connection', function (socket) {

            console.log('User connected!');
            clients[socket.id] = socket;

            socket.on('disconnect', function () {
                delete clients[socket.id];
                console.log('user disconnected');
            });

            socket.on('hash', function (msg) {

                console.log('Received message: ' + msg);
                var data = JSON.parse(msg);

                if (requestedHashes[data.hash]) { //if this hash is already requested --> just add current socketId to the list
                    requestedHashes[data.hash].push(socket.id);
                }
                else {
                    requestedHashes[data.hash] = [];
                    requestedHashes[data.hash].push(socket.id);
                    queueHelper.sendHashRequest(data);
                    console.log("sent '" + data.hash + "' to exchange!")
                }

            });

        });

        function handleWorkerResponse(data) {
            var requestedSockets = requestedHashes[data.hash];
            if(requestedSockets) {
                for (var i = 0; i < requestedSockets.length; i++) {

                    if (clients[requestedSockets[i]]) {
                        clients[requestedSockets[i]].emit('hash', data);
                    }
                }
                delete requestedHashes[data.hash];
                console.log('sent found password to all requesting clients');
            }
        }
    }


};
