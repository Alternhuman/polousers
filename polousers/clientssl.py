#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import ssl, reactor
from OpenSSL import SSL
import json, os, sys, logging
import shutil, errno



permission = oct(755)
umask = oct(22)

skeldir = '/etc/skel/.' #TODO: Get it from C

class Servlet(Protocol):
	def dataReceived(self, data):
		
		data_dict = json.loads(data.decode('utf-8'))
		params = data_dict["Params"].split(',',3)
		if data_dict["Command"] == "Create-Home":
			print("I shall now create the directory %s for %d %d with the utmost pleasure" % (params[0], int(params[1]), int(params[2])))
			create_homedir(params[0], int(params[1]), int(params[2]))

		self.transport.write(data)

	def create_homedir(self, name, uid, gid):
		
		if os.path.exists(name):
			logging.info("The directory %s already exists.", name)
			return

		try:
			shutil.copytree(skeldir, name)
		except OSError as e:
			if e.errno == errno.ENOTDIR:
				shutil.copy(src, name)
			else:
				logging.error("Directory not copied. Error %s" % e)

		for root, dirs, files in os.walk(name):
			for d in dirs:
				os.chown(os.path.join(root, d), uid, gid)
			for f in files:
				os.chown(os.path.join(root, f), uid, gid)

		try:
			os.chown(name, uid, gid)
		except OSError as e:
			log.error("Ownership could not be set: %s", e)

		try:
			os.chmod(name, int(permission,8))
		except OSError as e:
			log.error("Permission could not be set: %s", e)

		return

	def dataReceived(self, data):
		
		data_dict = json.loads(data.decode('utf-8'))
		params = data_dict["Params"].split(',',3)
		if data_dict["Command"] == "Create-Home":
			print("I shall now create the directory %s for %d %d with the utmost pleasure" % (params[0], int(params[1]), int(params[2])))
			self.create_homedir(params[0], int(params[1]), int(params[2]))

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

	if not os.path.exists('/var/run/marcopolo'):
		os.makedirs('/var/run/marcopolo')

	f = open("/var/run/marcopolo/polousersclient.pid", 'w')
	f.write(str(os.getpid()))
	f.close()

	if not os.path.exists('/var/log/marcopolo'):
		os.makedirs('/var/log/marcopolo')

	logging.basicConfig(filename="/var/log/marcopolo/polousersclient.log", level=logging.DEBUG)

	logging.info('Starting polousersclient')

	reactor.listenSSL(1343, factory, myContextFactory)
	reactor.run()