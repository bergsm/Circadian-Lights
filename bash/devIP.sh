#!/bin/bash

hostIP="$(hostname -I | head -c 10)255"

ping -b -c 10 $hostIP >/dev/null

arp -a >> network.list
