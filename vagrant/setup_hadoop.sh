#!/bin/bash

# 1. Install Java

sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install oracle-java7-installer


# 2. Setup hadoop group & user

sudo addgroup hadoop
sudo adduser --ingroup hadoop hduser


# 3. Setup hduser

su - hduser
ssh-keygen -t rsa -P ""
cat .ssh/id_rsa.pub >> .ssh/authorized_keys


# 5. Disable IPv6

sudo echo "net.ipv6.conf.all.disable_ipv6 = 1" >> /etc/sysctl.conf
sudo echo "net.ipv6.conf.default.disable_ipv6 = 1" >> /etc/sysctl.conf
sudo echo "net.ipv6.conf.lo.disable_ipv6 = 1" >> /etc/sysctl.conf

sudo sysctl -p


# 6. Install Hadoop
sudo add-apt-repository ppa:hadoop-ubuntu/stable
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install hadoop


# 7. Modify .bashrc
sudo cat bashrc_append.txt >> $HOME/.bashrc