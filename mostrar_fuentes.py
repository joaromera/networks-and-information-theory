#!/usr/bin/python

from scapy.all import *
from math import log2

S1 = {}

def info(p):
    return log2(1.0 / p)

def mostrar_fuente(S):
    N = sum(S.values())
    simbolos = sorted(S.items(), key=lambda x: -x[1])
    print("\n".join([ "%s : %.5f, %.5f" % (d,k/N,info(k/N)) for d,k in simbolos ]))
    print("H(S) = %.5f" % sum([k/N * info(k/N) for d,k in simbolos ]))
    print()

def callback(pkt):
    if pkt.haslayer(Ether):
        dire = "BROADCAST" if pkt[Ether].dst=="ff:ff:ff:ff:ff:ff" else "UNICAST"
        proto = pkt[Ether].type # El campo type del frame tiene el protocolo
        s_i = (dire, proto) # Aca se define el simbolo de la fuente
        if s_i not in S1: S1[s_i] = 0.0
        S1[s_i] += 1.0
    mostrar_fuente(S1)

sniff(prn=callback)
