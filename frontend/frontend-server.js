#!/usr/bin/env node

"use strict";

//configuration
var port = 8080; //default port

//node modules
var express = require('express');
var app = express();
var http = require('http').Server(app);

//Controller
var socketController = require('./controller/socket-controller');

function start() {

    if(process.argv.length > 3){
        console.log("usage: frontend-server.js [port]");
        return
    }else if(process.argv.length == 3){
        port = process.argv[2];
    }

    //returns static files automatically
    app.use(express.static('public'));

    socketController.start(http);

    http.listen(port, function(){
       console.log('Server is listening on port ' + port + '!');
    });

}

start();