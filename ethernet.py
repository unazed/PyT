"""
Ethernet structure for packet encapsulation.
"""

from packet import Packet


class Ethernet(Packet):
    def __init__(self, dst_mac, src_mac, data, crc, type_=False):
        super(Ethernet, self).__init__()
        self.dst_mac = dst_mac
        self.src_mac = src_mac
        self.type = type_ or "\x08\x00"  # \x08\x00 -> IPv4 
        self.data = data
        self.crc = crc

    def __str__(self):
        """
        Convert Ethernet structure to a transmissible form.
        
        /---------------------------------------------------------\
        |[0 - 5]|[6 - 12]|[12 - 14]|[15-60]|[61-1500?]|[1501-1504]|
        |DST MAC|SRC MAC |TYPE     |PADDING|DATA      | CRC/FCS   |
        \---------------------------------------------------------/
        
        """
        
        return "%s%s%s%s%s%s" % (self.dst_mac, self.src_mac, self.type,
                "\x00"*46, self.data[:1500], self.crc[:4])

    def __type__(self):
        """
        Return the unbound type of the class.
        """
        
        return Ethernet

    def __repr__(self):
        """
        Make informative display strings when object is listed e.g.
        
        >>> print(ether_packet_list) -> 
        ... [<Ethernet Packet (src=...) (dst=...) data=(...)>, <Ethernet Packet ...>]
        """
        
        _data = self.data[:13] + '...'
        return "<Ethernet Packet (src=%s) (dst=%s) (data=%s)>" %\
                            (
                                repr(self.src_mac),
                                repr(self.dst_mac),
                                repr(_data)
                            )

    @staticmethod
    def decapsulate(eth_packet):
        """
        Static-method meaning the class does not have to be bound in order
        to call this method, simply Ethernet.decapsulate(...).
        
        Decapsulates an Ethernet string into its component parts given by
        
        /---------------------------------------------------------\
        |[0 - 5]|[6 - 12]|[12 - 14]|[15-60]|[61-1500?]|[1501-1504]|
        |DST MAC|SRC MAC |TYPE     |PADDING|DATA      | CRC/FCS   |
        \---------------------------------------------------------/
        
        
        """
        
        if not isinstance(eth_packet, basestring):
            eth_packet = str(eth_packet)

        dst_mac = eth_packet[:6]
        src_mac = eth_packet[6:12]
        type_   = eth_packet[12:14]
        data    = eth_packet[60:-4]
        crc     = data[-4:]

        return dst_mac, src_mac, type_, data, crc

    def encapsulate(self):
        """
        Alias method in the case the user does not know you can call
        str(...) over the bound Ethernet class and retrieve a formatted
        string.
        """
        
        return self.__str__()
