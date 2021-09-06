"""
CustomPacket class

Provides: 
    - The package attributes used in the program
    - The methods to work with these attributes
    - The method output_format that provides the values to be consumed by the interface.

"""

import socket
from scapy.all import *
from process import Process

class CustomPacket: 

    def __init__(self,packet):
        self._ip_src = packet[0][1].src
        self._ip_dst = packet[0][1].dst
        self._port_src = packet[0][2].sport
        self._port_dst = packet[0][2].dport
        self._app_proto = self.get_app_proto(self.get_external_port())
        self._trans_proto = self.get_trans_proto(packet)
        self._size = self.get_size(packet)
        self._process = Process(self._ip_src,self._port_src,self._port_dst)
        
    
    def is_incoming(self):
        """ Define if the packet is incoming or outgoing from the interface."""
        if self._ip_src != get_if_addr(conf.iface):
            return True
        return False

    def get_trans_proto(self,packet):
        """ Define what transportation protocol the packet is using."""
        if packet.haslayer(TCP):
            return "TCP"
        if packet.haslayer(UDP):
            return "UDP"
        if packet.haslayer(ICMP):
            return "ICMP"

    def get_app_proto(self,port):
        """ Define what application protocol the packet is using.
            It uses the getservbyport from socket module to do this task.
        """
        try:
            return socket.getservbyport(port)
        except:
            return "others"

    def get_external_port(self):
        """ Define the external port.
            This info is passed to the get_app_proto method in the __init__ method.
        """
        if self._ip_src != get_if_addr(conf.iface):
            return self._port_src 
        else: 
            return self._port_dst

    def get_external_ip(self):
        """ Define the external IP.
            This info is used in the output_format method.
        """
        if self._ip_src != get_if_addr(conf.iface):
            return self._ip_src
        else:
            return self._ip_dst

    def get_server_dns(self,IP):
        """ Define the IP DNS if it exists."""
        try:
            return socket.gethostbyaddr(IP)[0]
        except:
            return IP
    
    def get_size(self,packet):
        """ Define the length of the packet in bytes."""
        return len(packet)
    
    def get_incoming(self):
        """ Define the size of the incoming data in a packet."""
        if self.is_incoming():
            return self._size
        else:
            return 0
    
    def get_outgoing(self):
        """ Define the size of the outgoing data in a packet."""
        if self.is_incoming():
            return 0
        else:
            return self._size
   
    def output_format(self):
        """ This method provide the information that is going to be consumed by the interface. """
        packet = {
            'Ip' : self.get_external_ip(),
            't_protocol' : self._trans_proto,
            'a_protocol' : self._app_proto,
            'proc_name'  : self._process._name,
            'incoming'   : self.get_incoming(),
            'outgoing'   : self.get_outgoing(),
            'size'       : self._size
        }

        return packet
   