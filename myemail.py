#!/bin/env python
# -*- coding: utf-8 -*-
 
 
import datetime
import smtplib
import os,sys
from email.mime.text import MIMEText
from email.mime.nonmultipart import MIMENonMultipart
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from optparse import OptionParser
 
 
 
 
EMAILHOME=sys.path[0]
#sender name and password
sendername=""
senderpass=""
#list of all receiver (include cc-receiver)
receiverlist=[]
receivertmplist=[]
receivercctmplist=[]
 
 
 
 
#get the username and pasword
#no try catch here
def getUserAndPass(senderfile):
    upf=open(senderfile)
    username=upf.readline()
    password=upf.readline()
    upf.close()
    return (username.strip(os.linesep),password.strip(os.linesep))
 
 
 
 
#get the receiver list
#return the list with no ''
def getReceiverList(filename):
    lif=open(filename)
    li=lif.readlines()
    lif.close()
    for x in range(len(li)):
        li[x]=li[x].strip().strip(os.linesep)
    while '' in li:
        li.remove('')
    return (li)
 
 
 
 
#get content of the mail
def getContent(filename):
    contenttmp=''
    if os.path.exists(filename):
        contentf=open(filename)
        contenttmp=contentf.read()
        contentf.close()
    return contenttmp
 
 
 
 
 
 #print ("start")
 
 
#parameters process
parser = OptionParser()
 
 
parser.add_option('-s', '--sender', dest='sender',
        help='file for sender of the mail', default=None)
parser.add_option('-r', '--receiver', dest='receiver',
        help='list file for receivers of the mail',default=None)
parser.add_option('-p', '--cc', dest='cc',
        help='list file for receivers of carbon copy', default=None)
parser.add_option('-t', '--title', dest='title',
        help='title of the email,string', default='Auto email')
parser.add_option('-c', '--content', dest='content',
        help='content of the mail,must be a file',default=None)
parser.add_option('-a', '--attach', dest='attach',
        help='attachment of the file',default=None)
parser.add_option('-n', '--nameattach', dest='nameattach',
        help='name for attachment of the file',default=None)
parser.add_option('-l', '--server', dest='server',
        help='log in to the server',default='smtp.163.com')
parser.add_option('-i', '--info', dest='info',
        help='information of the content,string,but not file',default='Auto email')
parser.add_option('-f', '--form', dest='form',
        help='form of the content,html or plain',default='plain')
 
 
(options, args) = parser.parse_args()
 
 
 
 
#get sender infor
if not options.sender:
    if os.path.exists(EMAILHOME+r'/sender.list'):
        (sendername,senderpass)=getUserAndPass(EMAILHOME+r'/sender.list')
        if sendername.strip()=="" or senderpass.strip()=="":
            print ("no sender!")
            exit(0)
    else:
        print ("no sender!")
        exit(0)
else:
    if os.path.exists(options.sender):
        (sendername,senderpass)=getUserAndPass(EMAILHOME+r'/sender.list')
        if sendername.strip()=="" or senderpass.strip()=="":
            print ("no sender!")
            exit(0)
    else:
        print ("the file for sender list does not exists!")
        exit(0)
 
 
         
#get list of all receiver
if not options.receiver:
    if os.path.exists(EMAILHOME+r'/receiver.list') or os.path.exists(EMAILHOME+r'/receivercc.list'):
        if os.path.exists(EMAILHOME+r'/receiver.list'):
            receivertmplist= getReceiverList(EMAILHOME+r'/receiver.list')
        if os.path.exists(EMAILHOME+r'/receivercc.list'):
            receivercctmplist= getReceiverList(EMAILHOME+r'/receivercc.list')
        receiverlist=receivertmplist+receivercctmplist
        if len(receiverlist)==0:
            print ("no receiver!")
            exit(0)
    else:
        print ("no receiver list file!")
        exit(0)
else:
    if os.path.exists(options.receiver) or os.path.exists(options.cc):
        if os.path.exists(options.receiver):
            receivertmplist= getReceiverList(options.receiver)
        if os.path.exists(options.cc):
            receivercctmplist= getReceiverList(options.cc)
        receiverlist=receivertmplist+receivercctmplist
        if len(receiverlist):
            #print ("no receiver from the list file!")
            #exit(0)
            receiverlist = ['zhangbo-nwnu@foxmail.com','zhangb@hengjun365.com']
    else:
        print ("receiver list file does not exist!")
        exit(0)
 
 
if  options.attach and not options.nameattach:
    print ("give a name to the attachment!")
    exit(0)
     
 
 
#make a mail   
mailall=MIMEMultipart()   
     
#content of the mail   
if options.content:
    mailcontent =getContent(options.content)
    mailall.attach(MIMEText(mailcontent,options.form,'utf-8'))
elif options.info:
    mailcontent = str(options.info)
    mailall.attach(MIMEText(mailcontent,options.form,'utf-8'))
 
 
#attachment of the mail   
if options.attach:
    mailattach =getContent(options.attach)
    if mailattach !='':
        contype = 'application/octet-stream'
        maintype,subtype=contype.split('/',1)
        attfile=MIMEBase(maintype,subtype)
        attfile.set_payload(mailattach)
        attfile.add_header('Content-Disposition','attachment',options.nameattach)
        print ("attach file prepared!")
        mailall.attach(attfile)
 
 
#title,sender,receiver,cc-receiver,
mailall['Subject']=options.title
mailall['From']=sendername
mailall['To']=str(receivertmplist)
if len(receivercctmplist) !=0:
    mailall['CC']=str(receivercctmplist)
 
 
 
 
#get the text of mailall
fullmailtext=mailall.as_string()
print ("prepare fullmailtext ok.")
mailconnect = smtplib.SMTP(options.server)
try:
    mailconnect.login(sendername,senderpass)
except Exception :
    print ("error when connect the smtpserver with the given username and password !")
    
    exit(0)
 
 
print ("connect ok!")
 
 
try:
    mailconnect.sendmail(sendername, receiverlist, fullmailtext)
except Exception:
    print ("error while sending the email!")
finally:
    mailconnect.quit()
 
 
print ('email to '+str(receiverlist)+' over.')
 
print ('***'*80)