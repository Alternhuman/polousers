# -*- coding: utf-8 -*-
from os.path import join, isabs
import logging

from six.moves import configparser

CONF_DIR = '/etc/polohomedir/'

TOMCAT_NAME = 'apache-tomcat-7.0.62'
PIDFILE_POLOUSERS = '/var/run/polousers.pid'
LOGGING_DIR = '/var/log/marcopolo'
PORT = 1343
CERT_DIR = '/etc/polohomedir/certs'
CERT_NAME = 'server.crt'
KEY_NAME = 'server.key'
CA_NAME = 'rootCA.pem'
LOGGING_LEVEL = 'DEBUG'
MAIN_PORT_INCREMENT = 10000
STOP_PORT_INCREMENT = 20000
SERVICE_NAME = "polousers"

default_values = {
    'TOMCAT_NAME':TOMCAT_NAME,
    'PIDFILE_POLOUSERS':PIDFILE_POLOUSERS,
    'LOGGING_DIR':LOGGING_DIR,
    'PORT':PORT,
    'CERT_DIR':CERT_DIR,
    'CERT_NAME':CERT_NAME,
    'KEY_NAME':KEY_NAME,
    'CA_NAME':CA_NAME,
    'LOGGING_LEVEL':LOGGING_LEVEL,
    'MAIN_PORT_INCREMENT':MAIN_PORT_INCREMENT,
    'STOP_PORT_INCREMENT':STOP_PORT_INCREMENT,
    'SERVICE_NAME':SERVICE_NAME,
}

config = configparser.RawConfigParser(default_values, allow_no_value=False)

POLOUSERS_FILE_READ = join(CONF_DIR, 'polousers.cfg')

try:
    with open(POLOUSERS_FILE_READ, 'r') as df:
        config.readfp(df)
        
        TOMCAT_NAME = config.get('polousers', 'TOMCAT_NAME')
        LOGGING_DIR = config.get('polousers', 'LOGGING_DIR')
        PORT = config.getint('polousers', 'PORT')
        CERT_DIR = config.get('polousers', 'CERT_DIR')
        CERT_NAME = config.get('polousers', 'CERT_NAME')
        KEY_NAME = config.get('polousers', 'KEY_NAME')
        CA_NAME = config.get('polousers', 'CA_NAME')
        LOGGING_LEVEL = config.get('polousers', 'LOGGING_LEVEL')
        MAIN_PORT_INCREMENT = config.getint('polousers', 'MAIN_PORT_INCREMENT')
        STOP_PORT_INCREMENT = config.get('polousers', 'STOP_PORT_INCREMENT')
        SERVICE_NAME = config.get('polousers', 'SERVICE_NAME')
except IOError as i:
    logging.warning("Warning! The configuration file could not be read. Defaults will be used as fallback")
except Exception as e:
    logging.warning("Unknown exception in configuration parser %s" % e)
