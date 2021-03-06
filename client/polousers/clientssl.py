#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from twisted.internet.protocol import Factory, Protocol
from twisted.internet import ssl, reactor

from OpenSSL import SSL
import json, os, sys, logging
import shutil, errno, stat
import xml.etree.ElementTree as ET
import six
import time

from polousers import conf

from marcopolo.bindings.polo import Polo, PoloException, PoloInternalException
#umask = 0022

skeldir = '/etc/skel/.'

class Servlet(Protocol):
    """
    A Protocol that listens for SSL connections and executes MarcoPolo-like commands
    """


    def startProtocol(self):
        logging.debug("Starting protocol")

    
    
    def dataReceived(self, data):
        """
        Process a new stream of information

        :param bytes data: The stream of information
        """
        data_dict = json.loads(data.decode('utf-8'))
        #The parameters must be separated by commas
        params = data_dict["Params"].split(',',3)
        if data_dict["Command"] == "Create-Home":
            """The response is acknowledged as soon as possible in order
             to avoid a long waiting time in the requesting node
            """
            self.transport.write(json.dumps({"OK":0}).encode('utf-8'))
            
            logging.debug("I shall now create the directory %s for %d %d with the utmost pleasure" % (params[0], int(params[1]), int(params[2])))
            
            retval = self.create_homedir(params[0], int(params[1]), int(params[2]))
            logging.debug(os.path.join(params[0], 'apache-tomcat-7.0.62'))
            if os.path.exists(os.path.join(params[0], 'apache-tomcat-7.0.62')):
                logging.debug("I shall now configure Tomcat")
                try:
                    self.configure_tomcat(os.path.join(params[0], 'apache-tomcat-7.0.62'), int(params[1]))
                except Exception as e:
                    logging.debug(e)
                    #self.transport.write(json.dumps({"Error":str(e)}).encode('utf-8'))
            if retval == 0:
                logging.debug("Created")
            if retval == 1:
                logging.debug("The directory was not created because it already exists")
        else:
            # Wrong command
            self.transport.write(json.dumps({"Error":1}).encode('utf-8'))

    def create_homedir(self, name, uid, gid):
        """
        Creates the home directory, setting the appropriate permissions
        
        :param str name: The path of the directory

        :param int uid: The uid of the owner

        :param int gid: The gid of the owner's main group
        """
        if os.path.exists(name):
            logging.debug("The directory %s already exists.", name)
            return 1

        try:
            shutil.copytree(skeldir, name)
        except OSError as e:
            #if e.errno == errno.ENOTDIR:
            #    logging#shutil.copy(src, name) TODO
            #else:
            logging.error("Directory not copied. Error %s" % e)
            return 2

        try:
            for root, dirs, files in os.walk(name):
                for d in dirs: os.chown(os.path.join(root, d), uid, gid)
                for f in files: os.chown(os.path.join(root, f), uid, gid)
        except Exception as e:
            logging.error("Something went wrong during chown. %s" % e)
            return 2

        try:
            os.chown(name, uid, gid)
        except OSError as e:
            logging.error("Ownership could not be set: %s", e)
            return 2

        try:
            os.chmod(name, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
        except OSError as e:
            logging.error("Permission could not be set: %s", e)
            return 0

        return 0

    def configure_tomcat(self, directory, uid):
        """
        Configures the local instance of Tomcat to work with a set of ports dedicated to the user.

        Tomcat uses the following ports:

        - 8080: The main port where services listen for connections. It is replaced by uid + 10000 
        - 8005: The shutdown port. It is replaced by uid + 20000

        :param str directory: The path of the Tomcat installation

        :param int uid: The uid of the user, which determines the number of the port
        """
        if not isinstance(uid, six.integer_types):
            error = None
            try:
                uid = int(uid, 10)
            except ValueError:
                error = True

            if error:
                raise Exception("Wrong uid value")

        server_xml = os.path.join(directory, 'conf/server.xml')
        logging.debug(server_xml)
        if not os.path.isfile(server_xml):
            raise Exception("Not found!")
        error = None
        
        try:
            tree = ET.parse(server_xml)
        except Exception:
            error = True
        if error:
            raise Exception("Error on parsing")

        root = tree.getroot()

        root.attrib["port"] = str(uid+conf.STOP_PORT_INCREMENT)

        ajp = root.find("./Service[@name='Catalina']/Connector[@protocol='AJP/1.3']")
        http = root.find("./Service[@name='Catalina']/Connector[@protocol='HTTP/1.1']")
        
        if http is None or ajp is None:
            raise Exception("Necessary tags elements not found in XML")
        
        http.attrib["port"] = str(uid)
        ajp.attrib["port"] = str(uid+conf.MAIN_PORT_INCREMENT)

        tree.write(server_xml)

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

polo_instance = None

def publish_service(service):
    global polo_instance
    published = False
    while not published:
        try:
            polo_instance = Polo()
            ret_value = polo_instance.publish_service(service, root=True, permanent=False)
            published = True
        except PoloInternalException as pi:
            logging.warning(pi)
            time.sleep(2)
        except PoloException as pe:
            logging.warning(pe)
            break;
        except Exception as e:
            logging.error(e)
            break
    else:
        logging.info("Service published with id %s" % ret_value)

def stopService(service):
    global polo_instance
    try:
        polo_instance.unpublish_service(service)
    except PoloInternalException as pi:
        logging.warning(pi)
    except PoloException as pe:
        logging.warning(pe)
    except Exception as e:
        logging.error(e)

def main(argv=None):
    """
    Starts the factory for SSL connections

    :param list argv: The parameters passed to the command-line entry point
    (minus the first one)
    """
    factory = Factory()
    factory.protocol = Servlet

    myContextFactory = ssl.DefaultOpenSSLContextFactory(
        os.path.join(conf.CERT_DIR, conf.KEY_NAME), os.path.join(conf.CERT_DIR, conf.CERT_NAME)
    )

    ctx = myContextFactory.getContext()

    ctx.set_verify(SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT,
        verifyCallback
    )

    ctx.load_verify_locations(os.path.join(conf.CERT_DIR, conf.CA_NAME))

    if not os.path.exists('/var/log/marcopolo'):
        os.makedirs('/var/log/marcopolo')

    logging.basicConfig(filename="/var/log/marcopolo/polousersclient.log", level=logging.DEBUG)

    logging.info('Starting polousersclient')

    reactor.addSystemEventTrigger('before', 'shutdown', stopService, conf.SERVICE_NAME)
    reactor.callWhenRunning(publish_service, conf.SERVICE_NAME)
    reactor.listenSSL(1343, factory, myContextFactory)
    reactor.run()

if __name__ == "__main__":
    main(sys.argv[1:])