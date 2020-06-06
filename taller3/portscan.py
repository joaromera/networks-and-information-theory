
#fixme: estoy suponiendo que los timeouts se decrementan solos con el clock de la compu. Así como está entra en un loop infinito y no printea el "hola" de tcp_udp_scan.
#!/usr/bin/python
#V1, se analizan los UDP y TCP a la vez.
#UDP no usa flags
#Abajo está la fuente original, pero acá está indentado: https://gist.github.com/zypeh/7079970
#fuente con los comportamientos: https://resources.infosecinstitute.com/port-scanning-using-scapy/#gref


import sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
 

numberOfPorts = 100

ip = sys.argv[1]


def udp_scan(dst_ip,dst_port,dst_timeout):
    packet = IP(dst=ip)/UDP(dport=dst_port)

    resp = sr1(packet, verbose=False,timeout = dst_timeout)
    
    # If the server sends no response to the client’s UDP request packet for that port,
    # it can be concluded that the port on the server is either open or filtered. No final state of the port can be decided.
    if resp is None:
        return "abierto|filtrado"   #fixme: acá borramos los reenvíos.
    
    # The client sends a UDP packet with the port number to connect to.
    # If the server responds to the client with a UDP packet, then that particular port is open on the server.
    elif (resp.haslayer(UDP)):
        return "abierto"
    
    # The client sends a UDP packet and the port number it wants to connect to, but the server responds with an ICMP 
    # port unreachable error type 3 and code 3, meaning that the port is closed on the server.
    elif(resp.haslayer(ICMP)):
        ICMPErrorType = int(resp.getlayer(ICMP).type)
        ICMPErrorCode = int(resp.getlayer(ICMP).code) 

        if(ICMPErrorType==3 and ICMPErrorCode==3):
            return "cerrado"
        
        # If ICMP error type 3 and code 1, 2, 9, 10, or 13, then that port on the server is filtered.
        elif(ICMPErrorType==3 and ICMPErrorCode in [1,2,9,10,13]):
            return "filtrado"

    return "ERROR: algo salió mal con el protocolo."

def tcp_scan(ip, dst_port, dst_timeout):
    packet = IP(dst=ip)/TCP(dport=dst_port, flags='S')
    
    resp = sr1(packet, verbose=False, timeout=dst_timeout)
    if resp is None:
        return "filtrado"
    elif resp.haslayer(TCP):
        tcp_layer = resp.getlayer(TCP)
        if tcp_layer.flags == 0x12:
            return ("abierto", tcp_layer.flags)     #fixme, ver que se devuelvan las flags
            sr1(IP(dst=ip)/TCP(dport=ports, flags='AR'), verbose=False, timeout=dst_timeout*5)  #fixme: dport. según la cátedra, debería tomar un arreglo de todos los puertos (habría que crear el arreglo), según Garuflax, hay que mandárselo sólo al puerto que está abierto. 
        elif tcp_layer.flags == 0x14:
            return("cerrado", tcp_layer.flags)      #fixme, ver que se devuelvan las flags

for  port in range(1, numberOfPorts):
    dst_timeout=0.2 #fixme: el timeout se usa para volver a retransmitir el mensaje si no tengo respuesta, se puede experimentar modificando el timeout a ver cántos UDP se consiguen. En la consigna usaba 0.2.  
    print(port, end =" ")   
    print("TCP", tcp_scan(ip, port, dst_timeout))
    print(port, end =" ")   
    print("UDP",udp_scan(ip, port, dst_timeout))