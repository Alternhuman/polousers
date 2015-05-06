#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import ssl, reactor
from OpenSSL import SSL
import json

class Servlet(Protocol):
	def dataReceived(self, data):
		
		data_dict = json.loads(data.decode('utf-8'))
		params = data_dict["Params"].split(',',3)
		if data_dict["Command"] == "Create-Home":
			print("I shall now create the directory %s for %d %d with the utmost pleasure" % (params[0], int(params[1]), int(params[2])))
		self.transport.write(data)


def verifyCallback(connection, x509, errnum, errdepth, ok):
	if not ok:
		print("Invalid certificate from subject ", x509.get_subject())
		return False
	else:
		return True

if __name__ == "__main__":
	factory = Factory()
	factory.protocol = Servlet

	myContextFactory = ssl.DefaultOpenSSLContextFactory(
        '/opt/certs/server.key', '/opt/certs/server.crt'
        )

	ctx = myContextFactory.getContext()

	ctx.set_verify(SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT,
	 	verifyCallback
	 	)

	ctx.load_verify_locations("/opt/certs/rootCA.pem")

	reactor.listenSSL(1343, factory, myContextFactory)
	reactor.run()