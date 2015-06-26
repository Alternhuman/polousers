# -*- coding: utf-8 -*-
import twisted.application
from twisted.application import internet
from twisted.internet import ssl
from twisted.internet.protocol import Factory
from OpenSSL import SSL
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor, defer
import os
from os import listdir, makedirs, path
from os.path import isfile, join
from io import StringIO
import sys, signal, json, logging
from twisted.internet.error import MulticastJoinError
import time
import pwd, grp
import re


from polousers.clientssl import Servlet
from polousers import conf
__author__ = 'Diego Martín'

application = twisted.application.service.Application("Polousers")

logging.basicConfig(filename=os.path.join(conf.LOGGING_DIR,'polousers.log'), level=conf.LOGGING_LEVEL.upper())#, format=conf.LOGGING_FORMAT)


def graceful_shutdown():
    """
    Stops the reactor gracefully
    """
    logging.info('Stopping service polod')

def verifyCallback(connection, x509, errnum, errdepth, ok):
    """
    The OpenSSL needs the callback to determine the validity of a certificate

    :param connection: The connection
    :param x509: A x509 object
    :param int errnum: The error number
    :param int errdepth: The depth of the error
    :param bool ok: Determines if the certificate is valid or not. 

    """
    if not ok:
        logging.warning("Invalid certificate from subject ", x509.get_subject())
        return False
    else:
        return True


def start_polousers():
	factory = Factory()
	factory.protocol = Servlet

	myContextFactory = ssl.DefaultOpenSSLContextFactory(
	    '/etc/polohomedir/certs/server.key', '/etc/polohomedir/certs/server.crt'
	    )

	ctx = myContextFactory.getContext()

	ctx.set_verify(SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT,
	    verifyCallback
	)

	ctx.load_verify_locations("/etc/polohomedir/certs/rootCA.pem")


	f = open("/var/run/polousersclient.pid", 'w')
	f.write(str(os.getpid()))
	f.close()

	if not os.path.exists('/var/log/marcopolo'):
	    os.makedirs('/var/log/marcopolo')

	logging.basicConfig(filename="/var/log/marcopolo/polousersclient.log", level=logging.DEBUG)

	logging.info('Starting polousersclient')

	reactor.listenSSL(1343, factory, myContextFactory)
	
	#reactor.run()
start_polousers()