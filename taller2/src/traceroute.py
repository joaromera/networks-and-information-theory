#!/usr/bin/python

import sys
import statistics
from scapy.all import *
from time import *

from functions import get_outliers

if len(sys.argv) <= 1:
    print("Modo de uso: sudo python3 traceroute.py <dirección destino>")
    exit()

destination = sys.argv[1]
packet_amount = 50 # amount of times a packet is sent with each TTL
hops_max = 30

responses = {}
for ttl in range(1, hops_max + 1):
    responses[ttl] = []

for i in range(packet_amount):
    for ttl in range(1, hops_max + 1):
        probe = IP(dst=destination, ttl=ttl) / ICMP()
        t_i = time()
        ans = sr1(probe, verbose=False, timeout=0.8)
        t_f = time()
        rtt = (t_f - t_i)*1000 # RTT in miliseconds
        if ans is not None:
            #if ttl not in responses: responses[ttl] = []
            responses[ttl].append((ans.src, rtt))
            if ans.src == probe.dst: break
        print("iteration: {} ttl: {} rtt: {}".format(i, ttl, rtt), end="\r") # Debugging

# Drop empty TTLs
responses = dict(filter(lambda e: e[1],responses.items()))

# Get for each TTL most used route
for ttl in responses.keys():
    ips = {}
    for (ip, _) in responses[ttl]:
        if ip not in ips: ips[ip] = 0
        ips[ip] = ips[ip] + 1
    most_used_ip = reduce(lambda x, y: x if x[1] >= y[1] else y, ips.items())[0]
    responses[ttl] = list(filter(lambda x : x[0] == most_used_ip, responses[ttl]))

# Get mean for each TTL
for ttl in responses.keys():
    responses[ttl] = (responses[ttl][0][0], statistics.mean([x[1] for x in responses[ttl]]))

# Get RTT between jumps
jumps_rtt = [x[1] for x in responses.values()]
for i in range(len(jumps_rtt)-1,0,-1):
    jumps_rtt[i] = jumps_rtt[i] - jumps_rtt[i - 1]

# Get outliers
is_outlier = get_outliers(jumps_rtt)

# Print results
print("{:3s} {:15s} {:15s} {:15s} {:10s}".format("TTL", "IP", "RTT", "RTT salto", "Outlier o negativo"))
for ((ttl, (ip, rtt)), jrtt, io) in zip(responses.items(), jumps_rtt, is_outlier):
    print("{:3d} {:15s} {:15f} {:15f} {:10b}".format(ttl, ip, rtt, jrtt, io))

positives_rtt_jumps = sum(1 if n > 0 else 0 for n in jumps_rtt)
print("\nCantidad de saltos RTT positivos: {}".format(positives_rtt_jumps))
print("\nCantidad de outliers: {}".format(sum(1 if b else 0 for b in is_outlier) - (len(jumps_rtt) - positives_rtt_jumps)))