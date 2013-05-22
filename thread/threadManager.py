#!/usr/bin/python
import time
from threading import Thread
from Queue import Queue

class threadManager():
  def __init__(self, realFunction, jobQ, workerNum):
    self.realFunction = realFunction
    self.jobQ = jobQ
    self.workerNum = workerNum

  def workerFunction(self):
    while True:
      job = self.jobQ.get()
      self.realFunction(job)
      self.jobQ.task_done()

  def start(self):
    for i in range(self.workerNum):
      worker = Thread(target=self.workerFunction)
      worker.setDaemon(True)
      worker.start()
    self.jobQ.join()
    time.sleep(1)
