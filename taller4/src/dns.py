import sys
from scapy.all import *

from functions import print_section


if len(sys.argv) <= 1:
    print("Modo de uso: sudo python3 dns.py <dirección destino>")
    exit()

qname = sys.argv[1]
dns = DNS(rd=1,qd=DNSQR(qname=qname, qtype="MX"))
udp = UDP(sport=RandShort(), dport=53)
ip = IP(dst="199.9.14.201") # b.root-servers.net ip

answer = sr1( ip / udp / dns , verbose=0, timeout=10)
if answer and answer.haslayer(DNS) and answer[DNS].qd.qtype == 15:
    print_section("ANSWER", answer[DNS].an)
    print_section("AUTHORITY", answer[DNS].ns)
    print_section("ADDITIONAL", answer[DNS].ar)
    