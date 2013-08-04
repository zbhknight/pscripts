""" EAP authentication handler

This module sents EAPOL begin/logoff packet
and parses received EAP packet 

"""

__all__ = ["EAPAuth"]

from socket import *
import os, sys, pwd

# init() # required in Windows
from eappacket import *

def diplay_packet(packet):
	print 'Ethernet Header Info: '
	print '\tFrom: ' + repr(packet[:6])
	print '\To: ' + repr(packet[6:12])
	print '\tType: ' + repr(packet[12:14])

fake = "\xaa\xbb\xcc\xdd\xee\x11"
fake2 = "\x00\x22\x68\x82\x2b\x4d"

class EAPAuth:
	def __init__(self, login_info):
		#self.client = socket(AF_PACKET, SOCK_RAW, htons(ETHERTYPE_PAE))
		self.client = socket(PF_PACKET, SOCK_RAW, ETHERTYPE_PAE)
		#self.client = socket(PF_PACKET, SOCK_RAW, 0x800)
		#self.client.bind((login_info[2], ETHERTYPE_PAE))
		self.client.bind((login_info[2], 0x888e))
		#self.client.bind((login_info[2], 0x800))
		self.mac_addr = self.client.getsockname()[4]
		self.ethernet_header = get_ethernet_header(self.mac_addr, PAE_GROUP_ADDR, ETHERTYPE_PAE)
		#self.ethernet_header = get_ethernet_header('\x00\xe0\xfc\x21\x72\xe8', '\x00\x1e\x68\xae\x25\x39', ETHERTYPE_PAE)
		#self.ethernet_header = get_ethernet_header('\x00\xe0\xfc\x79\x9a\x1b', PAE_GROUP_ADDR, ETHERTYPE_PAE)
	
	def set_broadcast(self):
		self.ethernet_header = get_ethernet_header(self.mac_addr, BROADCAST_ADDR, ETHERTYPE_PAE)

	def set_source(self):
		self.ethernet_header = get_ethernet_header(PAE_GROUP_ADDR, PAE_GROUP_ADDR, ETHERTYPE_PAE)

	def set_fake(self, src, dst):
		self.ethernet_header = get_ethernet_header(src, dst, ETHERTYPE_PAE)

	def set_header(self, mac):
		self.ethernet_header = get_ethernet_header(self.mac_addr, mac, ETHERTYPE_PAE)
	
	def send_start(self):
		eap_start_packet = self.ethernet_header + get_EAPOL(EAPOL_START)
		self.client.send(eap_start_packet)
	
	def send_logoff(self):
		logoff_packet = self.ethernet_header + get_EAPOL(EAPOL_LOGOFF) + '\x00'*2
		self.client.send(logoff_packet)

	def send_request_id(self):
		self.client.send(self.ethernet_header + get_EAPOL(EAPOL_EAPPACKET, get_EAP(EAP_REQUEST, 2, EAP_TYPE_ID)) + '\x00'*2)

	def send_request_pass(self):
		self.client.send(self.ethernet_header + get_EAPOL(EAPOL_EAPPACKET, get_EAP(EAP_REQUEST, 3, EAP_TYPE_H3C)) + '\x00'*37)

	def send_response_id(self, packet_id):
		self.client.send(self.ethernet_header + get_EAPOL(EAPOL_EAPPACKET, get_EAP(EAP_RESPONSE, packet_id, EAP_TYPE_ID, "\x06\x07bjQ7SE8BZ3MqHhs3clMregcDY3Y=\x20\x20"+ 'abcde')))
	
	def send_failure(self):
		self.client.send(self.ethernet_header + get_EAPOL(EAPOL_EAPPACKET, get_EAP(EAP_FAILURE, 6)))
