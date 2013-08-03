#!/usr/bin/python
#-*- coding=utf-8 -*-

import smtplib
import sys


class MyMail():
  def __init__(self, username, password, smtpSvr):
    self.username = username.split('@')[0]
    self.usermail = username
    self.password = password
    self.smtpSvr = smtpSvr

  def sendmail(self, destEmail, title, msg):
    server = smtplib.SMTP(self.smtpSvr)
    server.login(self.username, self.password)
    mail = """From: %s\r\nTo:%s\r\nsubject:%s\r\n\r\n%s""" % (self.usermail, ', '.join(destEmail), title, msg)
    server.sendmail(self.usermail, destEmail, mail)
    server.quit()
