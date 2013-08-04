#!/usr/bin/python

import netsnmp

class Snmp():
	def __init__(self, oid="sysDescr", Version=2, DestHost="localhost", Community="public"):
		self.oid = netsnmp.Varbind(oid)
		self.version = Version
		self.destHost = DestHost
		self.community = Community

	def query(self):
		try:
			result = netsnmp.snmpwalk(self.oid, Version=self.version, DestHost=self.destHost, Community=self.community)
		except Exception, e:
			print str(e)
			result = False
		return result
