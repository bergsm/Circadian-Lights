#!/bin/bash

ping -b -c 10 255.255.255.255 >/dev/null 2>&1
ping -c 10 255.255.255.255 >/dev/null 2>&1

arp -a >> network.list
