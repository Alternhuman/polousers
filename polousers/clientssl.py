#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import ssl, reactor
from OpenSSL import SSL
import json, os, sys, logging
import shutil, errno, stat
import xml.etree.ElementTree as ET
import os

#umask = 0022

skeldir = '/etc/skel/.' #TODO: Get it from C

class Servlet(Protocol):
	def dataReceived(self, data):
		
		data_dict = json.loads(data.decode('utf-8'))
		params = data_dict["Params"].split(',',3)
		if data_dict["Command"] == "Create-Home":
			print("I shall now create the directory %s for %d %d with the utmost pleasure" % (params[0], int(params[1]), int(params[2])))
			print("Creating")
			self.create_homedir(params[0], int(params[1]), int(params[2]))
			print(os.path.join(params[0], 'apache-tomcat-7.0.62'))
			if os.path.exists(os.path.join(params[0], 'apache-tomcat-7.0.62')):
				print("I shall now configure Tomcat")
				try:
					self.configure_tomcat(os.path.join(params[0], 'apache-tomcat-7.0.62'), int(params[1]))
				except Exception as e:
					self.transport.write(json.dumps({"Error":str(e)}).encode('utf-8'))
		print("Created")
		self.transport.write(json.dumps({"OK":0}).encode('utf-8'))

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
			os.chmod(name, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
		except OSError as e:
			log.error("Permission could not be set: %s", e)

		return

	def configure_tomcat(self, directory, uid):

		if not isinstance(uid, int):
			error = None
			try:
				uid = int(uid, 10)
			except ValueError:
				error = True

			if error:
				raise Exception("Wrong uid value")

		server_xml = os.path.join(directory, 'conf/server.xml')
		print(server_xml)
		if not os.path.isfile(server_xml):
			raise Exception("Not found!")
		error = None
		
		try:
			tree = ET.parse(server_xml)
		except Exception:
			error = True
		if error:
			raise Exception("Error on parsing")

		root=tree.getroot()

		root.attrib["port"] = str(uid+20000)

		ajp = root.find("./Service[@name='Catalina']/Connector[@protocol='AJP/1.3']")
		http = root.find("./Service[@name='Catalina']/Connector[@protocol='HTTP/1.1']")
		
		if http is None or ajp is None:
			raise Exception("Necessary tags elements not found in XML")
		
		http.attrib["port"] = str(uid)
		ajp.attrib["port"] = str(uid+10000)

		tree.write(server_xml)

	# def dataReceived2(self, data):
		
	# 	data_dict = json.loads(data.decode('utf-8'))
	# 	params = data_dict["Params"].split(',',3)
	# 	if data_dict["Command"] == "Create-Home":
	# 		print("I shall now create the directory %s for %d %d with the utmost pleasure" % (params[0], int(params[1]), int(params[2])))
	# 		self.create_homedir(params[0], int(params[1]), int(params[2]))

	# 	self.transport.write(data)


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
