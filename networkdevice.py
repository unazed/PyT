"""
Creates class for identifying general network devices.
"""

from hardwaredevice import HardwareDevice
from exceptions import DisabledHost
from exceptions import MultipleGateways
from exceptions import InvalidDiscoveryHost
from packet import Packet


class NetworkDevice(HardwareDevice):
    def __init__(self, network, ip_addr, is_gateway=False, **kwargs):
        super(NetworkDevice, self).__init__(**kwargs)

        self.network    = network
        self.ip_addr    = ip_addr

        if not self.network.gateway is None and is_gateway:
            raise MultipleGateways("There already exists a default gateway"
                                   " on the network.")

        self.is_gateway = is_gateway
        self.network.add_host(self)

        self.enabled    = True  # not to be confused with self.powered
        # this self.enabled defines wire[less] connectivity and whatnot
        # -however self.powered defines whether the hardware device has
        # -power being transmitted to it and is even able to drop or 
        # -queue packets.

        self.links      = []
        self.data_queue = []
        
        self.routing    = {}  # {destination: interface}
        
    def __repr__(self):
        """
        Allow for more user-friendly readability of object
        description
        """
        
        return "<NetworkDevice (IP address=%s)>" % self.ip_addr
    
    def _link_create(self, link):
        """
        Private method for links to call when they want to 
        link themselves against a network-device.
        """
        
        if not self.enabled:
            
            return False

        self.links.append(link)
        self.routing[link.get_host(self).ip_addr] = link
        
        return True

    def _link_queue_data(self, host, data, forward=None):
        """
        Private method for links to call when they need to
        queue or forward data from the host to another interface
        that is known by the routing tables on the device.
        """
        
        if not self.enabled:
            
            return False
        elif forward is not None and forward is not self.ip_addr:
            
            return self.routing[forward].send(self, data, forward)
        self.data_queue.append(data)
        
        return True

    def get_data(self):
        """
        Pop data from data-queue.
        """
        
        if not self.enabled or not self.powered:
            raise DisabledHost("Host is not turned on.")

        try:

            return self.data_queue.pop(0)
        except IndexError:
            
            return False

    def is_linked(self, host=None, ip_addr=None):
        """
        Check whether the host is linked with another
        IP address or host such as a router or a PC
        object.
        """
        
        if not self.enabled:
            raise DisabledHost("Host is not turned on.")

        for link in self.links:
            if link.get_host(self) is host:
                
                return True
            elif link.get_host(self).ip_addr == ip_addr:
                
                return True

        return False

    def has_route_to(self, ip_addr):
        """
        Check whether the host has a specific route to 
        a layer-3 IP address in the routing table.
        """
        
        if ip_addr in self.routing:
            
            return True
        
        return False

    def send_data(self, ip_addr, packet):
        """
        Send a packet to an IP address assuming the IP address
        is within the network and internal routing table.
        """
        
        if isinstance(packet, basestring):
            packet = Packet(packet)

        if not isinstance(packet, Packet):
            raise TypeError("Packet must be of 'Packet' class or a string.")

        if ip_addr not in [host.ip_addr for host in self.network.hosts]:
            raise LookupError("Host must be on the same network.")

        if ip_addr in self.routing:
            res = self.routing[ip_addr].send(host=self, data=packet, forward=ip_addr)

            return res

    def enable(self):
        """
        Enable wire[less] connectivity on the host
        """
        
        self.enabled = True

    def disable(self):
        """
        Disable wire[less] connectivity on the host
        """
        
        self.enabled = False

    def invert(self):
        """
        Invert wire[less] connectivity on the host
        Example: 1 -> 0 and 0 -> 1
        """
        
        self.enabled ^= 1

    def discover(self, ip_addr, _ext=False):
        """
        Discover the path to an IP address by asking all
        neighbouring links whether they have a direct or
        neighbouring link which provides a route to the
        IP address
        """
        
        if ip_addr == self.ip_addr:
            raise InvalidDiscoveryHost("You cannot discover yourself.")  # deep

        for link in self.links:
            other_host = link.get_host(self)

            if other_host.ip_addr == ip_addr:
                self.routing[ip_addr] = link
                
                return link

            elif other_host.is_linked(ip_addr):
                self.routing[ip_addr] = link
                
                return link

            else:
                if _ext == other_host:
                    continue
                link_ = other_host.discover(ip_addr, self)
                if not link_:
                    return False
                
                self.routing[ip_addr] = link
                
                return link
            
        return False
