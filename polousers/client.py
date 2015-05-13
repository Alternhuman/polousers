#!/usr/bin/env python3
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import json, logging
import os, sys
import shutil, errno

umask = 0022

if sys.version_info[0] < 3:
	permission = 0755 #TODO Bitwise operation
else:
	permission = 0o755

skeldir = '/etc/skel/.' #TODO: Get it from C

class Cliente(DatagramProtocol):

	def datagramReceived(self, data, address):
		host, port = address
		print("received %r from %s:%d" % (data, host, port))
		data_dict = json.loads(data.decode('utf-8'))
		params = data_dict["Params"].split(',',3)
		if data_dict["Command"] == "Create-Home":
			logging.info("Creating the directory %s for the user %d %d", params[0], int(params[1]), int(params[2]))
			create_homedir(params[0], int(params[1]), int(params[2])) #print("I shall create the directory %s for %d %d" % (params[0], int(params[1]), int(params[2])))


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
			os.chmod(name, permission)
		except OSError as e:
			log.error("Permission could not be set: %s", e)

		return


if __name__ == "__main__":

	if not os.path.exists('/var/run/marcopolo'):
		os.makedirs('/var/run/marcopolo')

	f = open("/var/run/marcopolo/polousersclient.pid", 'w')
	f.write(str(os.getpid()))
	f.close()

	if not os.path.exists('/var/log/marcopolo'):
		os.makedirs('/var/log/marcopolo')

	logging.basicConfig(filename="/var/log/marcopolo/polousersclient.log", level=logging.DEBUG)

	logging.info('Starting polousersclient')
	
	reactor.listenUDP(1343, Cliente())
	reactor.run()