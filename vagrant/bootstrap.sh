#!/usr/bin/env bash

#   Apache Packages
#   ---------------

apt-get update
apt-get install -y apache2
rm -rf /var/www
ln -fs /vagrant /var/www


#   Geeneral Packages
#   ---------------

apt-get install git
apt-get install python-pip
apt-get install vim


#   Hadoop Packages
#   ---------------

apt-get install software-properties-common
apt-get install python-software-properties

add-apt-repository ppa:webupd8team/java
apt-get update && sudo apt-get upgrade
apt-get install oracle-java7-installer

# Setup hadoop user
sudo addgroup hadoop
sudo adduser --ingroup hadoop hduser

sudo add-apt-repository ppa:hadoop-ubuntu/stable
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install hadoop
