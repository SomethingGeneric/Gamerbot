#!/usr/bin/env bash

ip a

usermod -p $(echo "toor" | openssl passwd -6 -stdin) root

[[ ! -d /etc/ssh ]] && mkdir -p /etc/ssh

mv /stuff/ssh* /etc/ssh/.
chmod 600 /etc/ssh/ssh_host*

[[ ! -d $HOME/.ssh ]] && mkdir -p $HOME/.ssh

cat /stuff/gb.pub >> $HOME/.ssh/authorized_keys

echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

groupadd discord

echo "@discord  hard    nproc   10" >> /etc/security/limits.conf
echo "@discord  hard    nofile  20" >> /etc/security/limits.conf

/usr/bin/sshd -De
