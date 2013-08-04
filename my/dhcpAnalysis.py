#!/usr/bin/python
import sys
import getopt
import re
import datetime

def ipRange():
	f = open('dhcpd.conf', 'rb')
	data = []
	for line in f:
		if line[:6] == 'subnet':
			data.append(line)
	f.close()

	for line in data:
		p1 = r'((\d{1,3}\.){3}(\d{1,3}))'
		p = r'.* ' + p1 + r'.* ' + p1
		m = re.match(p, line)
		if m:
			print m.group(1), m.group(4)

def inSubnet(net, mask, ip):
	nets = net.split('.')
	masks = mask.split('.')
	ips = ip.split('.')
	for i in range(4):
		nets[i] = int(nets[i])
		masks[i] = int(masks[i])
		ips[i] = int(ips[i])
	cal = []
	for i in range(4):
		cal.append(ips[i] & masks[i])
		if cal[i] != nets[i]:
			return False
	
	return True

def checkFreeIP(subnet, mask):
	f = open('dhcpd.leases', 'rb')
	data = [ line for line in f ]
	f.close()

	now = datetime.datetime.today() - datetime.timedelta(hours=8)
	expire = now - datetime.timedelta(hours=2)
	
	busy = []
	for i in range(len(data)-1, 0, -1):
		if data[i][0] == '}':
			i -= 1
			tmp = []
			tmpLine = data[i]
			while tmpLine[0:5] != 'lease':
				tmp.append(tmpLine)
				i -= 1
				tmpLine = data[i]
			tmp.append(tmpLine)

			if tmp[-3].find('ends'):
				splits = tmp[-3].split()
				ip = tmp[-1].split()[1]
				endTime = datetime.datetime.strptime(splits[2]+' '+splits[3][:-1], "%Y/%m/%d %H:%M:%S")
				if endTime > now and inSubnet(subnet, mask, ip):
					busy.append(ip)
				elif endTime < expire:
					break
	return list(set(busy))

if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:], "l")
	for items in opts:
		if items[0] == '-l':
			ipRange()
			sys.exit()
	
	print checkFreeIP(args[0], args[1])
