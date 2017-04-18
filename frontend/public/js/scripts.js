// author: sascha mlakar

'use strict';


var submitHash = document.getElementById('submitHash');
var hash = document.getElementById('hash');
var hashResult = document.getElementById('hashResult');


hash.focus();


submitHash.addEventListener('click', submitButtonEvent);
hash.addEventListener('keyup', submitEnterEvent);
hash.addEventListener('input', hashChangeEvent);


function submitButtonEvent(event) 
{
	console.log('clicked submitButton. hash: ' + hash.value);
	
	if (hashValidate(hash.value))
	{
		sendHash();
	}
}

function submitEnterEvent(event)
{
	var char = event.keyCode;

	if (char == 13)
	{
		console.log('pressed enter. hash: ' + hash.value);
		
		if (hashValidate(hash.value))
		{
			sendHash();
		}
	}
}

function hashChangeEvent()
{
	updateButton();
}

function hashValidate(md5hash)
{
	var pattern = /^[a-f0-9]{32}$/i;
	

	if(pattern.test(md5hash))
	{
		console.log('md5 hash valid');
		return true;
	}
	else
	{
		console.log('md5 hash invalid');
		return false;
	}	
}

function updateButton()
{
	if(hashValidate(hash.value))
	{
		submitHash.classList.remove('button-disable');
		submitHash.classList.add('button-enable');

		submitHash.disabled = false;
	}
	else
	{
		submitHash.classList.remove('button-enable');
		submitHash.classList.add('button-disable');

		submitHash.disabled = true;
	}
}

function sendHash()
{
	hashResult.innerHTML += '<br />crack md5 hash: ' + hash.value;

    // send hash request to the server
    if(socket){
        var data = {'hash': hash.value,
                    'type': "MD5"};
        socket.emit('hash', JSON.stringify(data));
        console.log("sent '" + data.hash + "' to webserver!");
    }
    else{
        alert('Websocket is not initialized');
    }
}

// websocket-section
// for further information see: http://socket.io/docs/client-api/
var socket;
createWebSocketConnection();
function createWebSocketConnection() {

	if (socket) {
		return;
	}
    socket = io(); //initialize websocket connection

    socket.on('hash', function(msg){
        //response from server
		console.log("Websocket: received data from server");
        hashResult.innerHTML += "<br />Message from " + msg.origin + ": password for the hash '" + msg.hash + "' is '" + msg.password + "'";
        
    });

    socket.on('connect', function(){
        //fired as soon as the client connects to the server
		console.log("Websocket: connected");
    	hashResult.innerHTML += "<br />Connection to server established!";
    });

    socket.on('error', function(){
        //fired as soon as an error occured
		console.log("Websocket: an error occured!");
        hashResult.innerHTML += "<br />An error occured!";
    });

    socket.on('disconnect', function(errorData){
        //fired as soon as the client disconnects
		console.log("Websocket: disconnected");
        hashResult.innerHTML += "<br />Client is disconnected!";
    });
}


