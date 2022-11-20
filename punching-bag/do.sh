#!/usr/bin/env bash

ip a

usermod -p $(echo "toor" | openssl passwd -6 -stdin) root

ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa
ssh-keygen -f /etc/ssh/ssh_host_dsa_key -N '' -t dsa

echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

/usr/bin/sshd -De
