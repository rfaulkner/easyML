#!/bin/bash

#   Ryan Faulkner, 2014
#   bobs.ur.uncle@gmail.com
#
#   Installer for hadoop + deps


# 1. Install Java

add-apt-repository ppa:webupd8team/java
apt-get update && sudo apt-get upgrade
# apt-get install -y oracle-java7-installer
apt-get install -y openjdk-7-jdk

# 2. Setup hadoop group & user

addgroup hadoop
adduser --ingroup hadoop hduser


# 3. Setup hduser

su - hduser
ssh-keygen -t rsa -P ""
cat .ssh/id_rsa.pub >> .ssh/authorized_keys


# 5. Disable IPv6

echo "net.ipv6.conf.all.disable_ipv6 = 1" >> /etc/sysctl.conf
echo "net.ipv6.conf.default.disable_ipv6 = 1" >> /etc/sysctl.conf
echo "net.ipv6.conf.lo.disable_ipv6 = 1" >> /etc/sysctl.conf

sysctl -p


# 6. Install Hadoop
add-apt-repository ppa:hadoop-ubuntu/stable
apt-get update && sudo apt-get upgrade
apt-get install hadoop


# 7. Modify .bashrc
cat bashrc_append.txt >> $HOME/.bashrc