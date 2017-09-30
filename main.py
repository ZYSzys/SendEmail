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

def sendmail(subject,msg,toaddrs,fromaddr,smtpaddr,password, fzip):
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

    data = open(fzip, 'rb')
    ctype, encoding = mimetypes.guess_type(fzip)
    maintype, subtype = ctype.split('/', 1)
    file_msg = email.MIMEBase.MIMEBase(maintype, subtype)
    file_msg.set_payload(data.read())
    data.close()
    email.encoders.encode_base64(file_msg)
    basename = os.path.basename(fzip)
    file_msg.add_header('Content-Disposition', 'attachment', filename=str(basename))

    mail_msg.attach(file_msg)
    mail_msg.attach(MIMEText(msg, 'html', 'utf-8'))
    try:
        s = smtplib.SMTP()
        s.connect(smtpaddr)  #连接smtp服务器
        s.login(fromaddr,password)  #登录邮箱
        s.sendmail(fromaddr, toaddrs, mail_msg.as_string()) #发送邮件
        s.quit()
        print 'Done!'
    except Exception as e:
       print e, "Error: unable to send email"
       print traceback.format_exc()

if __name__ == '__main__':
    fromaddr = "17367077526@163.com"
    smtpaddr = "smtp.163.com"
    toaddrs = ["1220736035@qq.com"]
    subject = "C++作业"
    password = ".........."
    msg = "C++作业"

    dirname = '201605070523'
    usr = u'物联网'
    fzip = dirname+usr+'161.zip'
    #z = ZipDir()
    #z.zip_dir(dirname, fzip)
    #fzip = '201605070523zys.zip'
    sendmail(subject,msg,toaddrs,fromaddr,smtpaddr,password,fzip)