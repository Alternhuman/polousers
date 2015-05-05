#!/usr/bin/env python3
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import json

class Cliente(DatagramProtocol):

	def datagramReceived(self, data, address):
		host, port = address
		print("received %r from %s:%d" % (data, host, port))
		#data_dict = json.loads(data.decode('utf-8'))
		#params = data_dict["Params"].split(',',3)
		#if data_dict["Command"] == "Create-Home":
		#	print("I shall create the directory %s for %d %d" % (params[0], int(params[1]), int(params[2])))


if __name__ == "__main__":
	reactor.listenUDP(1343, Cliente())
	reactor.run()