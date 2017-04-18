## Installationsanleitung ##

# node.js #
**node.js konfigurieren**

Folgende Module müssen in node installiert werden: 


- express
- socket.io
- amqplib

Die notwendigen Befehle sind:

    
	npm install express --save
	npm install socket.io --save
	npm install amqplib


**node.js starten**

    node frontend-server.js

oder, wenn supervisor installiert ist:

    supervisor frontend-server.js

    
# RabbitMQ #

** RabbitMQ installieren **

RabbitMQ findet sich unter folgender Adresse:
    
    https://www.rabbitmq.com/releases/rabbitmq-server/v3.6.2/rabbitmq-server-3.6.2-1.noarch.rpm

Zusätzlich ist die Sprache erlang zu installieren. Informationen dazu finden sich unter:


	https://www.erlang-solutions.com/resources/download.html


** RabbitMQ starten **

Starten des RabbitMQ-Servers:

    service rabbitmq-server start

Das Management Plugin in Betrieb nehmen:

    rabbitmq-plugins enable rabbitq_management


** RabbitMQ konfigurieren **

1. Öffnen des Management Plugins im Browser. Zumeist mit folgender Adresse:

	localhost:15672
	
2. Am unteren Ende des Bildschirms `Import / export definition`.
3. Hochladen der Datei `rabbitmq-configuration.json`.

** Testen **

1. Um die exchange Funktionalität zu testen, zuerst `consumer-test-worker.js` starten.
2. Danach das Script `producer-test-worker.js` starten.

# python #

Es muss auf dem Rechner `python` in Version 3 installiert sein.

Weiters müssen die python Module
 - redis
 - pika

zur Verfügung stehen. Installiert werden diese mit den folgenden zwei Befehlen:

	pip install redis
	pip install pika
	
Weiters werden folgende Module benutzt:
 - json
 - configparser

# redis #

** Installieren des redis Servers **

1. Ausführen des redis Installers. Run `redis-2.4.6-setup-64-bit.exe`.

2. Starten des redis Servers unter dem default Pfad: `C:\Program Files\Redis` (`redis-server.exe`).
	-> if you execute the redis-cli.exe you can open a shell to try the redis commands

3. Man vergleiche den Source Code im Eclipse-Projekt um zu sehen wie die redis Datenbank zugegriffen wird.

lib jedi to access redis server is in folder lib.
textfile with values is in textfile passwoerter.
 
Run redis mit python: `https://pypi.python.org/pypi/redis`.

** Redis set authentification **

Nach der redis Installation kann man die authentification im config file setzen.

Default config file location: `C:/Programm Files/Redis/conf/redis.conf`

Find in config file -> "# requirepass foobared" and replace it with "requirepass <yourpass>"

Now you have to restart the redis server

Insert the command "AUTH <yourpass>" to register you to the redis server

