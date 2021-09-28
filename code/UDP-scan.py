#! /usr/bin/python

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

dst_ip = "172.16.111.145"   # Victim-Kali
src_port = RandShort()
dst_port = 53

# 发送UDP+Port(n)
UDP_scan_resp = sr1(IP(dst=dst_ip)/UDP(sport=src_port,dport=dst_port),timeout=10)

# 无响应/其他拒绝反馈报文
if UDP_scan_resp is None:
    print("Open|Filtered")

# UDP+port(n) 响应数据
elif(UDP_scan_resp.haslayer(UDP)):
    print("Open")

elif(UDP_scan_resp.haslayer(ICMP)):

	# ICMP Error(Type 3,Code 3)
	if(int(UDP_scan_resp.getlayer(ICMP).type) == 3 and int(UDP_scan_resp.getlayer(ICMP).code) == 3):
		print("Closed")
	
	# ICMP Error(Type 3,Code 1/2/9/10/13)
	elif(int(UDP_scan_resp.getlayer(ICMP).type) == 3 and int(UDP_scan_resp.getlayer(ICMP).code) in [1, 2, 9, 10, 13]):
		print("Filtered")