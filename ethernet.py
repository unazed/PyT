"""
Ethernet structure for packet encapsulation.
"""

from packet import Packet


class Ethernet(Packet):
    def __init__(self, dst_mac, src_mac, type_, data, crc):
        super(Ethernet, self).__init__()
        self.dst_mac = dst_mac
        self.src_mac = src_mac
        self.type = type_
        self.data = data
        self.crc = crc

    def __str__(self):
        return "%s%s%s%s%s%s" % (self.dst_mac, self.src_mac, self.type,
                "\x00"*46, self.data[:1500], self.crc[:4])

    def __type__(self):
        return "Ethernet"

    @staticmethod
    def decapsulate(eth_packet):
        if isinstance(eth_packet, Ethernet):
            eth_packet = str(eth_packet)

        dst_mac = eth_packet[:6]
        src_mac = eth_packet[6:12]
        type_   = eth_packet[12:14]
        data    = eth_packet[64:-4]
        crc     = data[-4:]

        return dst_mac, src_mac, type_, data, crc

    def encapsulate(self):
        return self.__str__()
