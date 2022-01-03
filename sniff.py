
from scapy.all import sniff, TCP, UDP,packet
from custom_packets import CustomPacket
import time

""" 
   Sniff class

   Provides:
   - The method __init__ that receives the function that collect the data from the custom_packet method.
   - The method start that initiate the sniffing. 
   - The method custom_packet provides the filtred data to be collected by the controller.
   - The method __del__ that destruct the instance. 
"""

class Sniff: 
 
    _packet: CustomPacket
    _time_stamp: int

    def __init__(self,func):
        self._func = func

    def __del__(self) -> int:
        return int(round(time.time() * 1000))

    def start(self) -> int:
        """ This method start the execution of the sniff method from Scapy library."""
        self._time_stamp =  int(round(time.time() * 1000))
        sniff(filter="ip",prn=self.custom_packet)
        

    
    def verify_proto(self,packet: packet) -> bool:
        """ This method filters the packages to only be UDP and TCP."""
        if packet.haslayer(TCP) or packet.haslayer(UDP):
            return True
        return False

    def custom_packet(self,packet: packet) -> None:
        """ This method provides the filtred data to be collected by the controller."""
        if self.verify_proto(packet):
            self._packet = CustomPacket(packet)
            self._func(self._packet.output_format())
            
            
            
            
            