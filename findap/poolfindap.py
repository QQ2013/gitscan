#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import urllib2
import httplib
import traceback
import socket
import sys
import time
import multiprocessing
import os
import syslog
import string
def getHtml(url):
    try:
        page = urllib2.urlopen(url)
    except Exception, e: 
        syslog.syslog('failed to open %s' %(url))
        #print e
        html = "error"
    else: 
        try:
            html = page.read()
        except Exception, e: 
            syslog.syslog('failed to read %s' %(url))
            #print e
            html = "error"
    return html

def getApache(html):
    reg = r'core'
    apre = re.compile(reg)
    aplist = re.findall(apre,html)
    return len(aplist)

def poolscan(datas):
    pool = multiprocessing.Pool(processes = pid_num)
    for i in range(1,len(datas)):
        pool.apply_async(scan,(datas[i],))
        #print datas[i]
    pool.close()
    pool.join()

def scan(line): 
    html = getHtml(line)
    result = getApache(html)
    if result > 0:
        syslog.syslog( "find git bug in %s" %(line))
    else:
        syslog.syslog( "not git bug in %s" %(line))

def filescan(filename):
    file = open("./split/"+filename)
    lines = file.readlines()
    i = 0;
    total = len(lines)
    datas={};
    k=1;
    for  line in lines:
        line = line.split('\n')
        line = line[0]
        datas[k]=line;
        k=k+1
        if k==pool_num:
            syslog.syslog("scan %s to %d/%d" %(filename,i*pool_num,total))
            poolscan(datas)
            k=1;
            datas={};
            i=i+1
    #print datas
    poolscan(datas)
#main start

cmdline = sys.argv
pid_num = string.atoi(cmdline[2])
pool_num = string.atoi(cmdline[1])

timeout = 2
socket.setdefaulttimeout(timeout)
urllib2.socket.setdefaulttimeout(timeout)

syslog.openlog("findap")
pathlist = os.listdir("./split")
pathlist.sort()

#print pathlist
file_num = len(pathlist)
i = 0;
for file in pathlist:
    #print file
    syslog.syslog("scan file %d/%d:%s" %(i,file_num,file))
    filescan(file)
    i = i+1

#print 'all done'
