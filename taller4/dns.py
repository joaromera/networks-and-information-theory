import sys
from scapy.all import *


if len(sys.argv) <= 1:
    print("Modo de uso: sudo python3 traceroute.py <dirección destino>")
    exit()

dst = sys.argv[1]
dns = DNS(rd=1,qd=DNSQR(qname=dst))
udp = UDP(sport=RandShort(), dport=53)
ip = IP(dst="199.9.14.201") # b.root-servers.net ip

answer = sr1( ip / udp / dns , verbose=0, timeout=10)
if answer and answer.haslayer(DNS) and answer[DNS].qd.qtype == 1:
    print("ANSWER SECTION:")
    for i in range( answer[DNS].ancount):
        print(answer[DNS].an[i].rrname, answer[DNS].an[i].rdata)
    print("AUTHORITY SECTION:")
    for i in range( answer[DNS].nscount):
        print(answer[DNS].ns[i].rrname, answer[DNS].ns[i].rdata)
    print("ADDITIONAL SECTION:")
    for i in range( answer[DNS].arcount):
        print(answer[DNS].ar[i].rrname, answer[DNS].ar[i].rdata)