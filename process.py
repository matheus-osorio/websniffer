import psutil
import socket
from scapy.all import *

"""
    Process class

    Provides: 
    - The method to get the process name and PID.
"""

class Process:

    _pid: int
    _name: str

    def __init__(self,ip_src: str ,port_src: int, port_dst: int) -> None:
        self._pid = self.get_pid(ip_src,port_src,port_dst)
        self._name = self.get_proc_name(self._pid)
    
    def get_proc_name(self,pid: int) -> str:
        """ Get the process name """
        p = psutil.Process(pid)
        return p.name()

    def get_pid(self,ip_src: str,port_src: int,port_dst: int ) -> int:
        """ Get the process pid """
        port = port_src
        if ip_src != get_if_addr(conf.iface):
            port = port_dst
        for con in psutil.net_connections(kind="inet4"):
            if con.laddr[1] == port:
                return con.pid