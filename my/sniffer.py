#!/usr/bin/python

import sys
from socket import *

ETH_P_IP = 0x800

s = socket(PF_PACKET, SOCK_RAW, ETH_P_IP)
s.bind(("eth0", 0x888e))

while 1:
	p = s.recv(2024)
	print repr(p)
