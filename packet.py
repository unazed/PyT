"""
Defines the general packet class for packets transmitted across networks.
"""

class Packet(object):
    def __init__(self, *args):
        self.args = args

    def __str__(self):  # default string method
        return ''.join(self.args)

    def __repr__(self):
        return "<Packet: (length=%d), (type=%s)>" % (len(self.__str__()),
                self.__type__())
