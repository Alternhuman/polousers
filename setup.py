#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The polousers client
"""

from setuptools import setup, find_packages
from codecs import open
import os, subprocess, glob, sys

from distutils.core import setup
from distutils.command.clean import clean
from distutils.command.install import install


custom_polouser_params = [
                          "--polousers-disable-daemons",
                          "--polousers-no-start"
                         ]

init_bin = detect_init()

def detect_init():
    try:
        subprocess.check_call(["systemctl", "--version"], stdout=None, stderr=None, shell=False)
        return 0
    except (subprocess.CalledProcessError, OSError):
        return 1


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
        chmod(os.path.join("/etc/polohomedir/certs", cert), stat.S_IREAD | stat.S_IWRITE)

if __name__ == "__main__":

    polousers_params = []

    python_version = int(sys.version[0])


    polousers_params = [param for param in sys.argv if param in custom_polouser_params]
    sys.argv = list(set(sys.argv) - set(polousers_params))

    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
        long_description = f.read()

    data_files = [
                    ('/etc/polohomedir/certs', [glob.glob("certs/*")]),
                 ]

    if "--polousers-disable-daemons" not in polousers_params:
        
        daemon_path = "daemon/python"+str(python_version)

        if init_bin == 1:
            daemon_files = [
                            ('/etc/init.d', [os.path.join(daemon_path, "systemv/polousersd")])
                           ]
        else:
            daemon_files = [
                            ('/etc/systemd/system', [os.path.join(daemon_path, "systemd/polousers.service")])
                           ]
        if python_version == 2:
            twistd_files = [("/etc/polohomedir/daemon", [os.path.join(daemon_path, "twistd/polousers_twistd.tac")])]
            data_files.extend(twistd_files)

    data_files.extend(daemon_files)


    setup(
        name="polousers",
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

            'Topic :: Software Development :: Build Tools',

            'License :: OSI Approved :: MIT License',

            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',

        ],
        keywords="polousers ldap",
        packages=find_packages(),
        install_requires=[
            'Twisted==15.1.0',
            'zope.interface==4.1.2]'
            ],
        zip_safe=False,
        data_files=data_files,
        entry_points={
            'console_scripts': ['polousersd = polousers.clientssl:main',
                                ]
        }

    )

    set_cert_permissions()

    if "--polousers-disable-daemons" not in polousers_params:
        enable_service("polousersd")
        if "--polousers-no-start" not in polousers_params:
            start_service("polousersd")
    

    if not os.path.exists("/var/log/marcopolo"):
        os.makedirs('/var/log/marcopolo')
