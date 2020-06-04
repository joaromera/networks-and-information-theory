
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
 
ip = sys.argv[1]

numberOfPorts = 10



def tcp_udp_scan(dst_timeout):
    p = IP(dst=ip)/TCP(dport=port, flags='S')/UDP(dport=port) #fixme: supongo que la "/" es: agarrá este paquete o este otro, mandando flags en udp
    resp = sr1(p, verbose=False, timeout=dst_timeout) 
    print("hola")

    # If the server sends no response to the client's TCP request packer for that port.
    # it can be concluded that the port on the server is filtered. 
    # But considering that if the server sends no response to the client’s UDP request packet for that port,
    # the it can be concluded that the port on the server is either open or filtered. 
    #No final state of the port can be decided.

    if resp is None:
        retrans = []
        for count in range(0,3): #fixme: uso este rango de retransmisión porque es lo que se usó en las fuentes citadas arriba.
            retrans.append(sr1(IP(dst=ip)/UDP(dport=port), verbose=False, timeout=dst_timeout))
        for item in retrans:
            if (str(type(item))!="<type 'NoneType'>"): #fixme, creo que esto se puede cambiar por algo más declarativo
                tcp_udp_scan(dst_timeout)
        #If after retransmiting the server sends no response it can be concluded that the port on the server is either open or filtered. 
        #No final state of the port can be decided.
        return "TCP_or_UDP abierto|filtrado" #fixme: estos returns, antes eran print. pero no se que corresponde.
            
    # The client sends a UDP packet with the port number to connect to.
    # If the server responds to the client with a UDP packet, then that particular port is open on the server.
    elif resp.haslayer(UDP):   
        return "abierto"

    # The client sends a UDP packet and the port number it wants to connect to, but the server responds with an ICMP 
    # port unreachable error type 3 and code 3, meaning that the port is closed on the server.
    elif(esp.haslayer(ICMP)): #The client sends a UDP packet and the port number it wants to connect to, but the server responds with an ICMP port unreachable error type 3 and code 3, meaning that the port is closed on the server. fixme: ver si esto es lo que advierte la consigna.
        respICMP = resp.getlayer(ICMP)
        if(int(respICMP.type)==3):
            if(int(respICMP.code)==3): #The client sends a UDP packet and the port number it wants to connect to, but the server responds with an ICMP port unreachable error type 3 and code 3, meaning that the port is closed on the server
                return "cerrado"
            elif(int(respICMP.code) in [1,2,9,10,13]): #If the server responds to the client with an ICMP error type 3 and code 1, 2, 9, 10, or 13, then that port on the server is filtered.
                return "filtrado"
    

    #fixme: agregar descripoción de como funciona TCP.
    elif(resp.haslayer(TCP)):
        print("TCP", end =" ")
        tcp_layer = resp.getlayer(TCP)
        if tcp_layer.flags == 0x12:
            return ("abierto", tcp_layer.flags)
            #sr1(IP(dst=ip)/TCP(dport=port, verbose=False, flags='AR'), verbose=False, timeout=1) #fixme: no entiendo para que se vuelve a hacer esto acá. Así estaba en la consigna. No se si está bueno usar un timeout distinto para este caso.
        elif tcp_layer.flags == 0x14:
            return("cerrado", tcp_layer.flags)
    
    return "INESPERADO"        

for  port in range(1, numberOfPorts):
    dst_timeout=0.2 #fixme: el timeout se usa para volver a retransmitir el mensaje si no tengo respuesta, se puede experimentar modificando el timeout a ver cántos UDP se consiguen. En la consigna usaba 0.2.  
    print(port, end =" ")   
    tcp_udp_scan(dst_timeout)
            
   