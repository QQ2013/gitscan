#!/usr/bin/python
# -*- coding: utf-8 -*-
#查找IP地址归属地
#writer by keery_log
#Create time:2013-10-30
#Last update:2013-10-30
#用法: python chk_ip.py www.google.com |python chk_ip.py 8.8.8.8 |python chk_ip.py ip.txt
 
import signal
import urllib2
import json
import sys,os,re
import socket
 
if len(sys.argv) <= 1 :
    print "Please input ip address !"
    sys.exit(0)
 
def handler(signum, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, handler)
  
url = "http://ip.taobao.com/service/getIpInfo.php?ip="
 
#查找IP地址
def ip_location(ip):
    data = urllib2.urlopen(url + ip).read()
    datadict=json.loads(data)

 
    for oneinfo in datadict:
        if "code" == oneinfo:
            if datadict[oneinfo] == 0:
                return datadict["data"]["country"] + datadict["data"]["region"] + datadict["data"]["city"] + datadict["data"]["isp"]
def get_ip(line):
    reip = r'(\d+\.\d+\.\d+\.\d+)'
    reip = re.compile(reip)
    ip= re.findall(reip,line)
    return ip[0]  

#定义IP与域名正则
 
file_path = sys.argv[1]
fh = open(file_path,'r')
for line in fh.readlines():
    ip=get_ip(line)
    city_address = ip_location(ip)
    print line.strip() + "  :  " + city_address
