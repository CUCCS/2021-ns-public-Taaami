#! /usr/bin/python

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
dst_ip = "172.16.111.145"   # Victim-Kali
src_port = RandShort()
dst_port = 80

# 发送SYN+Port(n)
tcp_connect_scan_resp = sr1(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="S"),timeout=10)

# 无响应/其他拒绝反馈报文
if tcp_connect_scan_resp is None:
    print("Filtered")

elif(tcp_connect_scan_resp.haslayer(TCP)):

    # 回复SYN
    if(tcp_connect_scan_resp.getlayer(TCP).flags == 0x12):  #Flags: 0x012 (SYN, ACK)
        send_rst = sr(IP(dst=dst_ip)/TCP(sport=src_port,dport=dst_port,flags="AR"),timeout=10)
        print("Open")

    # 回复RST
    elif (tcp_connect_scan_resp.getlayer(TCP).flags == 0x14):   #Flags: 0x014 (RST, ACK)
        print ("Closed")