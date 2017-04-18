# MD5-Cracker #

Ein verteilter MD5-Passwort-Cracker.

## Teammitglieder ##

- Raphael Hartner
- Simone Hierhold
- Robert Ionescu
- Thomas Klampfl
- Sascha Mlakar
- Richard Raumberger
- Thomas Schönegger

## Gegenstand ##

Studium: Software Design

Gegenstand: Distributed Computing

Semester: Sommersemester 2016

## Architektur ##

![Architektur](http://i.imgur.com/scCOS9T.png)

## Protokolle ##

Protokoll User Interface - Frontend Server:

	{
		"hash": "912ec803b2ce49e4a541068d495ab570",
		"type": "MD5"
	}
 - `hash`: Der Hash-Wert, der aufgelöst werden soll.
 - `type`: Der Typ des Hash-Wertes.
 
Protokoll Frontend Server - User Interface:

	{
		"hash": "912ec803b2ce49e4a541068d495ab570",
		"type": "MD5",
		"origin": "<worker's identification>",
		"password": "<password>"
	}
 - `hash`: Der Hash-Wert, der aufgelöst werden soll.
 - `type`: Der Typ des Hash-Wertes.
 - `origin`: Der Ursprung dieser Nachricht. Dieser Wert identifiziert den Algorithmus mit dem das Passwort aufgelöst worden ist.
 - `password`: Das Passwort das dem Hash-Wert entspricht.
 
Protokoll Frontend Server - Broker:

	{
		"hash": "912ec803b2ce49e4a541068d495ab570",
		"type": "MD5",
		"origin": "frontend"
	}
 - `hash`: Der Hash-Wert, der aufgelöst werden soll.
 - `type`: Der Typ des Hash-Wertes.
 - `origin`: Der Ursprung dieser Nachricht. Der Frontend Server muss dieses Feld auf `frontend` setzen.

Protokoll Broker - Worker:

	{
		"hash": "912ec803b2ce49e4a541068d495ab570",
		"type": "MD5",
		"origin": "<origin>"
	}
 - `hash`: Der Hash-Wert, der aufgelöst werden soll.
 - `type`: Der Typ des Hash-Wertes.
 - `origin`: Der Ursprung dieser Nachricht. Der Wert `origin` ist immer auf die Identifikation des vorausgegangenen Workers, oder auf `frontend`, wenn kein Worker vorausgegangen ist, gesetzt.

Protokoll Worker - Broker:

	{
		"hash": "912ec803b2ce49e4a541068d495ab570",
		"type": "MD5",
		"origin": "<worker's identification>"
	}
 - `hash`: Der Hash-Wert, der aufgelöst werden soll.
 - `type`: Der Typ des Hash-Wertes.
 - `origin`: Der Ursprung dieser Nachricht. Wenn ein Worker eine Nachricht sendet, muss er dieses Feld zu seiner Identifikation setzen. Muss eindeutig unter allen Worker-Typen sein.

Protokoll Broker - Frontend Server:

	{
		"hash": "912ec803b2ce49e4a541068d495ab570",
		"type": "MD5",
		"origin": "<worker's identification>",
		"password": "<password>"
	}
 - `hash`: Der Hash-Wert, der aufgelöst werden soll.
 - `type`: Der Typ des Hash-Wertes.
 - `origin`: Der Ursprung dieser Nachricht. Dieses Feld identifiziert den Algorithmus, der benutzt wurde, um den Hash-Wert zu cracken.
 - `password`: Das Passwort, das dem Hash-Wert entspricht.

## Dateien und ihre Funktion ##

 - `/worker/database/worker.py`: Database Worker. Dies ist der erste Worker, der versucht den Hash-Wert aufzulösen. Der Datenbankworker sucht den MD5 Hash in der beigegebenen `redis`-Datenbank. Wenn die Datenbank den Hash schon enthält, wird eine Antwortnachricht mit dem routing key `found` zum Exchange gesandt. Andernfalls ist der routing key `md5.database`. Der Worker kann über die Datei `config.ini` konfiguriert werden.
 - `/worker/rainbow/worker.py`: Rainbow-Table Worker. Der zweite der Worker zum Auflösen des MD5-Hashes. Dieser Worker sucht den Hash-Wert in der beigefügten rainbow-Tabelle. Wenn diese den Wert des Hashes enthält, wird der routing key `found` an den Exchange gesandt. Sonst wird der routing key `md5.rainbow` verwendet.
Der Worker kann mittels der Datei `config.ini` konfiguriert werden.