#!/bin/bash
pacman -S openldap nss-pam-ldapd

echo "Performing some tests. Please enter username to try to authenticate with the server"
read username

ldapsearch -x -D uid=$username,ou=people,dc=DIA -W -H ldap://ldap1.cie.aulas.usal.es:389 -b dc=dia -s sub uid=$username

echo "Starting nslcd.service"

systemctl enable nslcd.service
systemctl start nslcd.service

#echo "Testing connection"

#getent passwd