import sys

from functions import *

arguments_amount = len(sys.argv)

if arguments_amount <= 1:
    print("Modo de uso: sudo python3 dns.py DOMAIN [SERVER_IP]")
    exit()

qname = sys.argv[1]
starting_ip = "198.41.0.4" if arguments_amount == 2 else sys.argv[2] # use a.root-server.net as default
server_ips = []
server_ips.append(starting_ip)

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
        if answer[DNS].arcount:
            for reg in answer[DNS].ar.iterpayloads(): # Add servers ipv4 to continue searching
                if reg.type == 1:
                    server_ips.append(reg.rdata)
    print()