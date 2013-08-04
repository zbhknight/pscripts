#!/usr/bin/python

from multiprocessing import Process, Queue, Pool
import time
import subprocess
import sys
from snmp import Snmp

q = Queue()
oq = Queue()
ips = []
num_workers = 10

class HostRecord():
	def __init__(self, ip=None, mac=None, snmp_response=None):
		self.ip = ip
		self.mac = mac
		self.snmp_response = snmp_response

	def __repr__(self):
		return "[Host Record('%s', '%s', '%s')]" % (self.ip, self.mac, self.snmp_response)

def find(i, q, oq):
	while True:
		time.sleep(0.1)
		if q.empty():
			sys.exit()
			print "Process Number: %s Exit" % i

		ip = q.get()
		print "Process Number: %s" % i
		ret = subprocess.call("ping -c 1 %s" % ip, shell=True, stdout=open('/dev/null', 'w'), stderr=sys.stdout)
		
		if ret == 0:
			print "%s: is alive" % ip
			oq.put(ip)
		else:
			print "Process Number: %s get no response for %s" % (i, ip)
			pass

def snmp_query(i, out):
	while True:
		time.sleep(0.1)
		if out.empty():
			sys.exit()
			print "Process Number: %s Exit" % i
		
		ipaddr = out.get()
		s = Snmp(DestHost=ipaddr, Community="jurassic")
		h = HostRecord()
		h.ip = ipaddr
		h.snmp_response = s.query()
		print str(h)
		return h

def main():
	f = open(sys.argv[1], 'r')
	ips = [ line[:-1] for line in f ]
	f.close()
	try:
		for ip in ips:
			q.put(ip)
	finally:
		for i in range(num_workers):
			p = Process(target=find, args=[i, q, oq])
			p.start()
		for i in range(num_workers):
			pp = Process(target=snmp_query, args=[i, oq])
			pp.start()
	
	p.join()

if __name__ == "__main__":
	main()
