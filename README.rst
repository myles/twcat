TwCat
=====

TwCat is a port of `Last.fm`_'s IRCcat_ to twitter.

Run TwCat
*********

``twcat -u twitter_username -p twitter_password``

Example configuration
*********************

You can store the configuration file in your home directory under
``~/.twcat.cfg`` or just reference it with ``twcat -c twcat.cfg``.

::
	
	[twcat]
	username = twcat_test
	password = div17kam
	
	host = 0.0.0.0
	port = 12345
	
	verbosity = 2
	log_file = /tmp/twcat.log

Example netcat commands
***********************

Send a status message::
	
	echo "Hello World from TwCat." | netcat -c 127.0.0.1 12345

Send a direct message::
	
	echo "d @username Hello World from TwCat." | netcat -c 127.0.0.1 12345
	# This will send a direct message to `username`.
	echo "d @username1 @username2 Hello World from TwCat." | netcat -c 127.0.0.1 12345
	# This will send a direct message to `username1` and `username2`.

.. _`Last.fm`: http://last.fm/
.. _IRCcat: http://github.com/RJ/irccat