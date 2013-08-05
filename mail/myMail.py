#!/usr/bin/python #-*- coding=utf-8 -*-

import email
import getpass
import os
import smtplib
import sys


class MyMail():
  def __init__(self, username, password, smtpSvr):
    self.main_msg = None
    self.username = username.split('@')[0]
    self.usermail = username
    self.password = password
    self.smtpSvr = smtpSvr
    self.server = smtplib.SMTP(self.smtpSvr)

  def sendmail(self, destEmail, title, msg):
    self.server.login(self.username, self.password)
    mail = """From: %s\r\nTo:%s\r\nsubject:%s\r\n\r\n%s""" % (self.usermail, ', '.join(destEmail), title, msg)
    self.server.sendmail(self.usermail, destEmail, mail)
    self.server.quit()

  def add_base(self, filename):
    #构建MIMEMultipart对象作为根容器
    if not self.main_msg:
      self.main_msg = email.MIMEMultipart.MIMEMultipart()

    #构建MIMEBase对象作为文件附件并附加到根容器
    contype = 'application/octet-stream'
    maintype, subtype = contype.split('/', 1)

    #读入文件内容并且格式化
    with open(filename, 'rb') as data:
      file_msg = email.MIMEBase.MIMEBase(maintype, subtype)
      file_msg.set_payload(data.read())
    email.Encoders.encode_base64(file_msg)

    #设置附件头
    basename = os.path.basename(filename)
    file_msg.add_header('Content-Disposition', 'attachment', filename=basename)

    self.main_msg.attach(file_msg)

  def add_text(self, text, txt_type="plain"):
    #构建MIMEMultipart对象作为根容器
    if not self.main_msg:
      self.main_msg = email.MIMEMultipart.MIMEMultipart()

    text_msg = email.MIMEText.MIMEText(text, txt_type)
    self.main_msg.attach(text_msg)

  def send_mime(self, destEmail, title):
    if not self.main_msg:
      return False
    self.main_msg['From'] = self.usermail
    self.main_msg['To'] = ', '.join(destEmail)
    self.main_msg['Subject'] = title
    self.main_msg['Date'] = email.Utils.formatdate()

    full_text = self.main_msg.as_string()
    self.server.login(self.username, self.password)
    self.server.sendmail(self.usermail, destEmail, full_text)
    self.server.quit()

def main():
  usermail = raw_input("usermail:")
  #set_spyder_echo(False)
  password = getpass.getpass("password:")
  #set_spyder_echo(True)
  sendto = raw_input("send to:")
  stmpserver = raw_input("smtpserver:")
  msg = raw_input("text:")
  filename = raw_input("filename:")

  m = MyMail(usermail, password, stmpserver)
  m.add_base(filename)
  m.add_text(msg)
  m.send_mime([sendto], "test")

if __name__ == "__main__":
  main()
