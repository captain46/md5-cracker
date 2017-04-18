Readme to run redis project
-----------------------------------------------------------------------------------------
Install redis server

1.Download and run redis installer from http://redis.io/
2.Start redis server with the executable located in the installation directory

----------------------------------------------------------------------------------------

Redis set authentication

After the redis installation you can set the authentication in the config file

Default config file location <redis-install-directory>/conf/redis.conf
Find in config file -> "# requirepass foobared" and replace it with "requirepass <yourpass>"
Restart the redis server

insert the command "AUTH <yourpass>" to register you to the redis server

