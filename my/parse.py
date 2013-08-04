#!/usr/bin/python

import sys
import re
import datetime
import shlex
import subprocess
import MySQLdb
from os import path

exIP = ['222.200.191.253', '1.3.6.1', '172.18.41.178']

def getData(filename):
	try:
		comm = 'grep -n ========== ' + filename
		args = shlex.split(comm)
		lineNum = int(subprocess.check_output(args).split('\n')[-2].split(':')[0])
		wcNum = int(subprocess.check_output(['wc', filename]).split()[0])
		number = wcNum - lineNum
		comm = 'tail -n ' + str(number) + ' ' + filename
		args = shlex.split(comm)
		data = subprocess.check_output(args).split('\n')
	except:
		f = open(filename, 'rb')
		data = [ line for line in f ]
		f.close()
	
	f = open(filename, 'ab')
	f.write('='*80+'\n')
	f.close()
	
	result = []
	for line in data:
		unit = parseLine(line)
		if unit:
			result.append(unit)

	return result

def parseLine(line):
	timeP = r'([a-zA-Z]{3}\s\d{1,2}\s(\d{2}:){2}\d{2})'
	ipP = r'((\d{1,3}\.){3}\d{1,3})'
	pattern = timeP + r'\s' + ipP + r'.*?' + ipP + r'(.*)'
	m = re.match(pattern, line)
	if m:
		return (m.group(1), m.group(5), m.group(7))

def getTime(string):
	year = datetime.datetime.today().year
	time = datetime.datetime.strptime(string+' '+str(year), "%b %d %H:%M:%S %Y")
	return time

def packup(data):
	final = {}
	for item in data:
		if not item[1] in exIP:
			if final.has_key(item[1]):
				final[item[1]][1] = getTime(item[0])
				final[item[1]][2].append(item[2])
			else:
				final[item[1]] = [getTime(item[0]), 0, []]
	
	return final

def insertDB(final, filename):
	db = MySQLdb.connect('localhost', 'root', '8817793', 'payroll')
	c = db.cursor()
	for key, argv in final.items():
		destIP = path.basename(filename)	
		sourceIP = key
		startTime = argv[0]
		endTime = argv[1]
		comms = argv[2]
		c.execute('insert into watch_login (sourceIP, destIP, startTime, endTime) values (%s,%s,%s,%s)', (sourceIP, destIP, startTime, endTime))

		lastId = c.lastrowid
		commList = [ (lastId, comm) for comm in comms ]
		c.executemany('insert into watch_command (ip_id, comm) values (%s, %s)', commList)

if __name__ == '__main__':
	argv = sys.argv[1:]
	for a in argv:
		data = getData(a)
		final = packup(data)
		insertDB(final, a)
