"""
Copyright 2009 Myles Braithwaite <me@mylesbraithwaite.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import re
import os
import socket
import logging
import ConfigParser

from optparse import OptionParser

import twitter

username_re = re.compile('@[0-9a-zA-Z]+')
direct_re = re.compile('d\s+')

class TwitterBridge(object):
	def __init__(self, username, password, host='127.0.0.1', port=12345, offline=False):
		self.username = username
		self.password = password
		
		self.api = twitter.Api(self.username, self.password)
		
		self.host = host
		self.port = port
		
		self.offline = offline
	
	def run(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((self.host, int(self.port)))
		s.listen(1)
		
		while 1:
			conn, addr = s.accept()
			logging.info('Client connected.')
			data = conn.recv(1024)
			if not data: break
			logging.info('Data received.')
			self.parse(data)
	
	def parse(self, data):
		if data.startswith('d '):
			# Is a Direct message
			usernames = [ u.replace('@', '') for u in username_re.findall(data) ]
			
			for username in usernames:
				message = username_re.sub('', data)
				message = direct_re.sub('', message, 1)
				logging.info('Sending direct message to `%s`.' % username)
				status = self.api.PostDirectMessage(username, message)
				logging.info('Direct message sent with id %s.' % status.id)
		else:
			logging.info('Sending status message.')
			status = self.api.PostUpdate(data)
			logging.info('Status message sent with id %s.' % status.id)

def main():
	parser = OptionParser(usage='%prog [options]')
	parser.add_option('-u', '--username',
		action='store',
		dest='username',
		help='Twitter username.')
	parser.add_option('-p', '--password',
		action='store',
		dest='password',
		help='Twitter password.')
	parser.add_option('-c', '--config',
		action='store',
		dest='config_file',
		help='Configuration file.')
	parser.add_option('-v', '--verbosity', 
		action='store', 
		dest='verbosity', 
		default='1',
		type='choice', 
		choices=['0', '1', '2'],
		help='Verbosity level; 0=minimal output, 1=normal output, 2=all output')
	parser.set_defaults()
	
	options, args = parser.parse_args()
	
	level = { '0': logging.WARN, '1': logging.INFO, '2': logging.DEBUG }
	
	config = ConfigParser.ConfigParser()
	
	try:
		config_file = os.environ['HOME'] + '/.twcat.cfg'
		open(config_file, 'r')
		config.read(config_file)
	except IOError:
		return '...'
	
	if options.config_file:
		config.read(options.config_file)
	
	if config.has_section('twcat'):
		log_filename = config.get('twcat', 'log_file', None)
		logging.basicConfig(level=level[config.get('twcat', 'verbosity', 1)], filename=log_filename, format='[%(asctime)s] %(levelname)s "%(message)s"')
		bridge = TwitterBridge(
			config.get('twcat', 'username'),
			config.get('twcat', 'password'),
			config.get('twcat', 'host', '0.0.0.0'),
			config.get('twcat', 'port', 12345))
	elif options.username and options.password:
		logging.basicConfig(level=level[options.verbosity], format="%(name)s: %(levelname)s: %(message)s")
		bridge = TwitterBridge(options.username, options.password)
	else:
		return '...'
	
	bridge.run()

if __name__ == '__main__':
	main()