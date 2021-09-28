#! /usr/bin/python

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
dst_ip = "172.16.111.1"   # Gateway-Debian
src_port = RandShort()
dst_port = 80

# 发送FIN+Port(n)
tcp_fin_scan_resp = sr1(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="F"),timeout=10)

# 无响应/其他拒绝反馈报文
if tcp_fin_scan_resp is None:
    print("Open|Filtered")

# 回复RST
elif(tcp_fin_scan_resp.haslayer(TCP)):
    if (tcp_fin_scan_resp.getlayer(TCP).flags == 0x14):   #Flags: 0x014 (RST, ACK)
        print ("Closed")

# ICMP Error(Type 3,Code 1/2/3/9/10/13)
elif(tcp_fin_scan_resp.haslayer(ICMP)):
	if(int(tcp_fin_scan_resp.getlayer(ICMP).type)==3 and int(tcp_fin_scan_resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
		print("Filtered")