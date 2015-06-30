#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The marcopolo-users client
"""

from setuptools import setup, find_packages
from codecs import open
import os, subprocess, glob, sys

from distutils.command.clean import clean
from distutils.command.install import install
import stat

custom_polouser_params = [
                          "--polousers-disable-daemons",
                          "--polousers-no-start"
                         ]

def detect_init():
    try:
        subprocess.check_call(["systemctl", "--version"], stdout=None, stderr=None, shell=False)
        return 0
    except (subprocess.CalledProcessError, OSError):
        return 1

init_bin = detect_init()

def enable_service(service):
    sys.stdout.write("Enabling service " + service +"...")
    if init_bin == 0:
        subprocess.call(["systemctl", "enable", service], shell=False)
    else:
        subprocess.call(["update-rc.d", "-f", service, "remove"], shell=False)
        subprocess.call(["update-rc.d", service, "defaults"], shell=False)
    
    sys.stdout.write("Enabled!")

def start_service(service):
    sys.stdout.write("Starting service " + service + "...")
    if init_bin == 0:
        subprocess.call(["systemctl", "start", service], shell=False)
    else:
        subprocess.call(["service", service, "start"], shell=False)

    sys.stdout.write("Started!")

def set_cert_permissions():
    for cert in os.listdir("/etc/polohomedir/certs"):
        os.chmod(os.path.join("/etc/polohomedir/certs", cert), stat.S_IREAD | stat.S_IWRITE)

    os.chmod("/etc/polohomedir/certs", stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)

if __name__ == "__main__":

    polousers_params = []

    python_version = int(sys.version[0])


    polousers_params = [param for param in sys.argv if param in custom_polouser_params]
    
    sys.argv = [arg for arg in sys.argv if arg not in polousers_params]
    
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
        long_description = f.read()

    data_files = []
    cert_files =  [
                    ('/etc/polohomedir/certs', glob.glob("etc/polohomedir/certs/*")),
                 ]

    if "--polousers-disable-daemons" not in polousers_params:
        
        daemon_path = "daemon/python"+str(python_version)

        if init_bin == 1:
            daemon_files = [
                            ('/etc/init.d/', [os.path.join(daemon_path, "systemv/polousersd")])
                           ]
        else:
            daemon_files = [
                            ('/etc/systemd/system/', [os.path.join(daemon_path, "systemd/polousers.service")])
                           ]
        if python_version == 2:
            twistd_files = [("/etc/polohomedir/daemon/", [os.path.join(daemon_path, "twistd/polousers_twistd.tac")])]
            data_files.extend(twistd_files)
            
        data_files.extend(daemon_files)
    
    data_files.extend(cert_files)
    
    setup(
        name="marcopolo-users",
        provides=["polousers"],
        version='0.0.1',
        description="The polousers client",
        long_description=long_description,
        url="marcopolo.martinarroyo.net",
        author="Diego Martín",
        author_email="martinarroyo@usal.es",
        license="MIT",
        classifiers=[
            'Development Status :: 3 - Alpha',

            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',

            'Topic :: System :: Systems Administration :: Authentication/Directory',

            'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',

            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
            'Natural Language :: English',

        ],
        keywords="polousers ldap",
        packages=find_packages(),
        install_requires=[
            "Twisted==15.1.0",
            "zope.interface==4.1.2",
            "marcopolo",
            "marcopolo.bindings",
            "cffi==0.9.2",
            "characteristic==14.3.0",
            "cryptography==0.8.2",
            "pyasn1==0.1.7",
            "pyasn1-modules==0.0.5",
            "pycparser==2.12",
            "pyOpenSSL==0.15.1",
            "service-identity==14.0.0",
            "six==1.9.0",
        ],
        zip_safe=False,
        data_files=data_files,
        entry_points={
            'console_scripts': ['polousersd = polousers.clientssl:main']
        }
    )
    
    if "install" in sys.argv:
        set_cert_permissions()
        if "--polousers-disable-daemons" not in polousers_params:
            enable_service("polousersd")
            if "--polousers-no-start" not in polousers_params:
                start_service("polousersd")
    
        if not os.path.exists("/var/log/marcopolo"):
            os.makedirs('/var/log/marcopolo')
