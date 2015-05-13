#!/usr/bin/env python3
# -*- coding: utf-8
from os import kill, remove
import os, signal

PIDFILE = '/var/run/marcopolo/polousersclient.pid'

f = open(PIDFILE, 'r')
pid = f.read()
f.close()
kill(int(pid), signal.SIGTERM)
os.remove(PIDFILE)