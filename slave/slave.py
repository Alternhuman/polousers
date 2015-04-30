#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, defer

import sys, os, json

sys.path.append('/opt/marcopolo/')
sys.path.append('/opt/marcousers/')
sys.path.append('/home/martin/TFG/workspaces/polousers/slave')

#from polousers_conf import conf

class Conf:
	PIDFILE_POLOUSERS = '/var/run/polousers/polousers.pid'
	LOGGING_DIR = '/var/log/polousers'
	PORT = 1343
conf = Conf()
class Slave(DatagramProtocol):

	def __init__(self):
		pass

	def StartProtocol(self):
		pass

	def datagramReceived(self, data, address):
		data_arr = json.loads(data.decode('utf-8'))

		params = self.decode_params(data_arr["Params"])
		home = params["home"]
		uid = params["uid"]
		gid = params["gid"]

		if not os.path.exists(home):
			os.makedirs(home)
			os.chown(home, uid, gid)

	def decode_params(self, params):
		args = params.split(',',3)
		return {"home":args[0], "uid":int(args[1]), "gid": int(args[2])}


if __name__ == "__main__":
	
	pid = os.getpid()
	
	if not os.path.exists('/var/run/polousers'):
		os.makedirs('/var/run/polousers')
	

	f = open(conf.PIDFILE_POLOUSERS, 'w')
	f.write(str(pid))
	f.close()

	#logging.basicConfig(filename=conf.LOGGING_DIR+'polousers.log', level=conf.LOGGING_LEVEL.upper(), format=conf.LOGGING_FORMAT)
	server = reactor.listenUDP(conf.PORT, Slave())
	#reactor.addSystemEventTrigger('before', 'shutdown', graceful_shutdown)
	reactor.run()