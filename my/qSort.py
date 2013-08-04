#!/usr/bin/python

import sys

def qSort(nums, low, high):
	if low >= high:
		return nums
	key = nums[low]
	front = low
	back = high
	while back > front:
		while nums[back] >= key and back > front:
			back -= 1
		if back > front:
			tmp = nums[back]
			nums[back] = nums[front]
			nums[front] = tmp
			#print nums
		
		while nums[front] <= key and back > front:
			front += 1
		if back > front:
			tmp = nums[back]
			nums[back] = nums[front]
			nums[front] = tmp
			#print nums
	
	#print "Turn End"
	
	qSort(nums, low, front-1)
	qSort(nums, back+1, high)

if __name__ == '__main__':
	argv = sys.argv[1:]
	for i in range(len(argv)):
		argv[i] = int(argv[i])
	qSort(argv, 0, len(argv)-1)
	print argv
