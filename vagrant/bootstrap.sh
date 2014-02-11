#!/usr/bin/env bash

#   Core Packages
#   -------------

apt-get update
apt-get install -y apache2
apt-get install -y libapache2-mod-wsgi

rm -rf /var/www
ln -fs /vagrant /var/www
apt-get install -y gfortran libopenblas-dev liblapack-dev
apt-get install -y g++


#   General Packages
#   ---------------

apt-get install -y git
apt-get install -y vim
apt-get install -y redis-server
apt-get install -y curl


#   MySQL
#   -----

apt-get install -y mysql-server
apt-get install -y mysql-client

# For now do this part manually

# mysqladmin -u root -h localhost password '{%mysql_password%}'
# mysqladmin -u root -h {%hostname%} password '{%mysql_password%}'


#   Python Packages
#   ---------------

apt-get install -y python-dev
apt-get install -y python-pip
apt-get install -y python-numpy python-scipy
apt-get install -y python-pydoop

apt-get -y install software-properties-common
apt-get -y install python-software-properties
