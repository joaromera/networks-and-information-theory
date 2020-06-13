import sys

from functions import *


if len(sys.argv) <= 1:
    print("Modo de uso: sudo python3 dns.py <dirección destino>")
    exit()

qname = sys.argv[1]
server_ips = []
server_ips.append("199.9.14.201") # b.root-servers.net ip

while server_ips:
    server_ip = server_ips.pop()
    print("QUESTION TO: {:s}".format(server_ip))
    answer = send_dns_mx_querry(server_ip, qname)
    if answer and answer.haslayer(DNS) and answer[DNS].qd.qtype == 15:
        print_section("ANSWER", answer[DNS].an)
        print_section("AUTHORITY", answer[DNS].ns)
        print_section("ADDITIONAL", answer[DNS].ar)
        if answer[DNS].ancount: # I finish when i get an answer
            break
        for reg in answer[DNS].ar.iterpayloads(): # Add servers ipv4 to continue searching
            if reg.type == 1:
                server_ips.append(reg.rdata)
    print()