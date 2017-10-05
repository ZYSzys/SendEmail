#!/usr/bin/env python
#-*- coding: utf-8 -*-

__author__ = 'ZYSzys'

import os
import smtplib
import traceback
import mimetypes
import email.MIMEBase
from zipfiles import ZipDir
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def Trans(fzip):
	data = open(fzip, 'rb')
	ctype, encoding = mimetypes.guess_type(fzip)
	maintype, subtype = ctype.split('/', 1)
	file_msg = email.MIMEBase.MIMEBase(maintype, subtype)
	file_msg.set_payload(data.read())
	data.close()
	email.encoders.encode_base64(file_msg)
	basename = os.path.basename(fzip)
	file_msg.add_header('Content-Disposition', 'attachment', filename=str(basename))
	return file_msg

def SendMail(subject,msg,toaddrs,fromaddr,smtpaddr,password, fzip):
    '''
    @subject:邮件主题
    @msg:邮件内容
    @toaddrs:收信人的邮箱地址
    @fromaddr:发信人的邮箱地址
    @smtpaddr:smtp服务地址，可以在邮箱看，比如163邮箱为smtp.163.com
    @password:发信人的邮箱密码
    '''
    mail_msg = MIMEMultipart()
    if not isinstance(subject,unicode):
        subject = unicode(subject, 'utf-8')
    mail_msg['Subject'] = subject
    mail_msg['From'] =fromaddr
    mail_msg['To'] = ','.join(toaddrs)

    mail_msg.attach(Trans(fzip))
    mail_msg.attach(MIMEText(msg, 'html', 'utf-8'))
    try:
        s = smtplib.SMTP()
        s.connect(smtpaddr)  #连接smtp服务器
        s.login(fromaddr,password)  #登录邮箱
        s.sendmail(fromaddr, toaddrs, mail_msg.as_string()) #发送邮件
        s.quit()
        print 'Send Done!'
    except Exception as e:
       print e, "Error: unable to send email"
       print traceback.format_exc()

if __name__ == '__main__':
	smtpaddr = "smtp.163.com"
	fromaddr = "17367077526@163.com"
	password = ".........."

	toaddrs = []
	to = str(raw_input("Send to (1220736035@qq.com): "))
	toaddrs.append(to)

	subject = raw_input("Subject (C++作业): ")
	msg = subject

	dirname = raw_input('which directory (201605070523): ')
	usr = u'物联网'
	fzip = dirname+usr+'161.zip'

	z = ZipDir()
	z.zip_dir(dirname, fzip)
	SendMail(subject,msg,toaddrs,fromaddr,smtpaddr,password,fzip)
	print 'Completed!'
