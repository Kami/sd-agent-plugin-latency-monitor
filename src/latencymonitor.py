import os
import re
import sys
import subprocess
import ConfigParser

class latencymonitor:
	def __init__(self):
		# Compile frequently used regular expressions
		if sys.platform == 'linux2':
			self.packetStatsRe = re.compile(r'(\d+) packets transmitted, (\d+) received, (.*?)% packet loss, time (\d+)ms')
			self.responseStatsRe = re.compile(r'rtt min/avg/max/mdev = (\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+) ms')
			
		elif sys.platform.find('freebsd') != -1:
			self.packetStatsRe = re.compile(r'(\d+) packets transmitted, (\d+) packets received, (.*?)% packet loss')
			self.responseStatsRe = re.compile(r'round-trip min/avg/max/(stddev|std-dev) = (\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+) ms')

		self.ipv4Re = re.compile(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
		self.ipv6Re = re.compile(r'^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$', re.IGNORECASE)
		
		# Read the plugin config file
		path = os.path.dirname(os.path.realpath(__file__))
		config = ConfigParser.ConfigParser()
		config.read(os.path.join(path, 'latencymonitor.cfg'))
		
		self.__config = {}
		self.__config['packetCount'] = config.get('General', 'packet_count')
		self.__config['hosts'] = config.items('Hosts')
	
	def run(self):
		try:
			response = {}
			for entry in self.__config['hosts']:
				address = entry[1]

				if re.match(self.ipv4Re, address) != None:
					command = 'ping'
				elif re.match(self.ipv6Re, address) != None:
					command = 'ping6'
				else:
					# Not a valid IPv4 or IPv6 address, skip this iteration
					continue

				response[address] = subprocess.Popen([command, '-c', self.__config['packetCount'], address], stdout = subprocess.PIPE, close_fds = True).communicate()[0]
		
		except Exception, e:
			return None
			
		latencyStatus = self.parseResponse(response)
		return latencyStatus
	
	def parseResponse(self, response):
		latencyStatus = {}
		# Loop over responses and parse the data
		for address in response:
			packetStats = re.search(self.packetStatsRe, response[address])
			responseStats = re.search(self.responseStatsRe, response[address])
			
			# Valid response
			if packetStats != None:
				latencyStatus[address] = {}
				latencyStatus[address]['trans_packets'] = packetStats.group(1)
				latencyStatus[address]['recv_packets'] = packetStats.group(2)
				latencyStatus[address]['packet_loss'] = packetStats.group(3)
				
				if responseStats != None:
					latencyStatus[address]['response_min'] = responseStats.group(2)
					latencyStatus[address]['response_max'] = responseStats.group(4)
					latencyStatus[address]['response_avg'] = responseStats.group(3)
				else:
					latencyStatus[address]['response_min'] = ''
					latencyStatus[address]['response_max'] = ''
					latencyStatus[address]['response_avg'] = ''
					
		return latencyStatus