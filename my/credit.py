#!/usr/bin/python

N = int(raw_input())

for i in range(N):
	C = int(raw_input())
	I = int(raw_input())
	items = raw_input().split()

	toSort = [ (i, int(items[i])) for i in range(len(items)) ]
