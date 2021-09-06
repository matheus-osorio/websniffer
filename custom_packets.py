"""
CustomPacket class

Provides: 
    - The package attributes used in the program
    - The methods to work with these attributes
    - The method output_format that provides the values to be consumed by the interface.

"""

import socket
from struct import unpack
from scapy.all import Packet,IP,TCP,UDP,ICMP, get_if_addr, conf
from process import Process

class CustomPacket: 

    _src_ip: str
    _dst_ip: str
    _src_port: int
    _dst_port: int
    _app_protocol : str 
    _trans_protocol : str 
    _process : Process
    _size: int


    def __init__(self,pkt: Packet) -> None:  
        self._src_ip = pkt[IP].src
        self._dst_ip = pkt[IP].dst
        self._src_port, self._dst_port  = self.get_ports(pkt)
        self._app_protocol = self.get_app_protocol()
        self._trans_protocol = self.get_trans_protocol(pkt)
        self._size = self.get_size(pkt)
        self._process = Process(self._src_ip,self._src_port,self._dst_port)
        
    def get_ports(self,pkt: Packet) -> str:
        """ Get the ports from the packet. """

        if pkt.haslayer(TCP):
            return pkt[TCP].sport , pkt[TCP].dport
        if pkt.haslayer(UDP):
            return pkt[UDP].sport , pkt[UDP].dport
    
    def is_incoming(self) -> bool:
        """ Define if the packet is incoming or outgoing from the interface."""
        if self._src_ip != get_if_addr(conf.iface):
            return True
        return False

    def get_trans_protocol(self,pkt: Packet) -> str:
        """ Define what transportation protocol the packet is using."""
        if pkt.haslayer(TCP):
            return "TCP"
        if pkt.haslayer(UDP):
            return "UDP"
        if pkt.haslayer(ICMP):
            return "ICMP"

    def get_app_protocol(self) -> str:
        """ Define what application protocol the packet is using.
            It uses the getservbyport from socket module to do this task.
        """
        try:
            return socket.getservbyport(self.get_external_port())
        except:
            return "others"
        
    def get_external_port(self) -> int:
        """ Define the external port.
            This info is used inside the get_app_protocol method .
        """
        if self._src_ip != get_if_addr(conf.iface):
            return self._src_port
        else: 
            return self._dst_port

    def get_external_ip(self) -> str:
        """ Define the external IP.
            This info is used in the output_format method.
        """
        if self._src_ip != get_if_addr(conf.iface):
            return self._src_ip
        else:
            return self._dst_ip

    def get_server_dns(self) -> str:
        """ Define the IP DNS if it exists."""
        try:
            return socket.gethostbyaddr(self.get_external_ip())[0]
        except:
            return IP
    
    def get_size(self,pkt: Packet) -> int:
        """ Define the length of the packet in bytes."""
        return len(pkt)
    
    def get_incoming(self) -> int:
        """ Define the size of the incoming data in a packet."""
        if self.is_incoming():
            return self._size
        else:
            return 0
    
    def get_outgoing(self) -> int:
        """ Define the size of the outgoing data in a packet."""
        if self.is_incoming():
            return 0
        else:
            return self._size

    def ip2long(self,ip) -> int:
        """ Convert an IP string to long """
    
        packedIP = socket.inet_aton(ip)
        return unpack("!L", packedIP)[0]
    
   
    def output_format(self) -> dict:
        """ This method provide the information that is going to be consumed by the interface. """
        packet = {
            'Ip' : self.ip2long(self.get_external_ip()),
            't_protocol' : self._trans_protocol,
            'a_protocol' : self._app_protocol,
            'proc_name'  : self._process._name,
            'incoming'   : self.get_incoming(),
            'outgoing'   : self.get_outgoing(),
            'size'       : self._size
        }

        return packet
   