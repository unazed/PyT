"""
Defines the general packet class for packets transmitted across networks.
"""

class Packet(object):
    def __init__(self, *args):
        self.args = args

    def __repr__(self):
        """
        Makes a more user-friendly representation of the repr() output or
        when seen implicitly such as when you print the bound instance.
        """
        
        return "<Packet: (length=%d), (type=%s) >" %\
                (
                    len(str(self)),
                    type(self)
                )
        
        
# NOTE: might reconsider making a class, 
# -this simply has 2 dunder methods and 
# -a fairly useless concept for existence
# -as it is only for organizing certain 
# -packets like Ethernet packets under
# -a common parent.
