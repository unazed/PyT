"""
Defines inheritance class which distributes hardware properties to nodes.
"""

from exceptions import UnablePortConnection


class HardwareDevice(object):
    def __init__(self, mac_addr, label, nports, power_usage=0):
        mac_addr = ''.join(chr(int(c, 16)) for c in mac_addr.split(':'))
        # convert hexadecimal formatted MAC address to proper bytes.
        
        self.mac_addr = mac_addr
        self.label = label
        self.nports = nports
        self.ports = {-1: None}  # {index: hardware}
        self.power_usage = power_usage
        self.powered = True

    def _connect_port(self, hardware):
        """
        Connects a piece of hardware to the hardware port for direct
        hardware I/O over a standard such as 802.3 or 802.11/*
        """
        
        if max(self.ports.keys())+1 > self.nports:
            return False
        self.ports[max(self.ports.keys())+1] = hardware
        return True
