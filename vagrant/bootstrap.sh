#!/usr/bin/env bash

#   Apache Packages
#   ---------------

apt-get update
apt-get install -y apache2
rm -rf /var/www
ln -fs /vagrant /var/www


#   General Packages
#   ---------------

apt-get install -y git
apt-get install -y python-pip
apt-get install -y vim
apt-get install -y vim
apt-get install -y redis-server
apt-get install -y python-redis


#   Hadoop Packages
#   ---------------

apt-get -y install software-properties-common
apt-get -y install python-software-properties

add-apt-repository ppa:webupd8team/java
apt-get -y update && sudo apt-get upgrade
apt-get -y install oracle-java7-installer

# Setup hadoop user
sudo addgroup hadoop
sudo adduser --ingroup hadoop hduser

add-apt-repository ppa:hadoop-ubuntu/stable
apt-get -y update && sudo apt-get upgrade
apt-get -y install hadoop
