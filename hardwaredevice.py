"""
Defines inheritance class which distributes hardware properties to nodes.
"""

from exceptions import UnablePortConnection


class HardwareDevice(object):
    def __init__(self, mac_addr, label, nports, power_usage=0):
        self.uf_mac_addr = mac_addr
        mac_addr = ''.join(chr(int(c, 16)) for c in mac_addr.split(':'))
        print(mac_addr)
        self.mac_addr = mac_addr


        self.label = label

        self.nports = nports
        self.ports = {-1: None}  # index: hardware

        self.power_usage = power_usage

    def _connect_port(self, hardware):
        if max(self.ports.keys())+1 > self.nports:
            return False
        self.ports[max(self.ports.keys())+1] = hardware
        return True
