Latency Monitor plugin
======================
Simple `Server Density`_ agent plugin for monitoring network latency and packet loss, inspired by SmokePing_.

Sample config file
==================
The values can be changes in the ``latencymonitor.cfg`` file::

  [General]
  packet_count = 5	# The number of packets to send
  
  [Hosts]
  ip_address_1 = 10.0.0.3
  ip_address_2 = 91.189.94.156
  ip_address_3 = 2001:05c0:1400:000b:0000:0000:0000:4cf7

* packet_count - how many packets to send to each host
* Hosts - In this section you put the addresses of the hosts you want to monitor (both IPv4 and IPv6 addresses are supported, but for IPv6 to work, you need IPv6 connectivity on your server)

How long it takes for the plugin to complete depends on the packet_count variable and the number of hosts you monitor.

Sample output
=============
This is how dictionary returned by this plugin might look like (yes, it's a dictionary of dictionaries)::

  {'latencymonitor': {'91.189.94.156': {'packet_loss': '0', 'response_max': '2.432', 'response_min': '46.606', 'recv_packets': '5', 'response_avg': '49.351', 'trans_packets': '5'}, '10.0.0.3': {'packet_loss': '0', 'response_max': '0.567', 'response_min': '0.762', 'recv_packets': '5', 'response_avg': '1.891', 'trans_packets': '5'}}}

*Note: Plugin should work on both Linux and FreeBSD although, FreeBSD is currently not officially supported by Server Density.*

.. _Server Density: http://www.serverdensity.com/
.. _SmokePing: http://oss.oetiker.ch/smokeping/