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

        self.enabled    = True

        self.links      = []
        self.data_queue = []
        
        self.routing    = {}  # {destination: interface}

    def _link_create(self, link):
        if not self.enabled:
            return False

        self.links.append(link)
        self.routing[link.get_host(self).ip_addr] = link
        return True

    def _link_queue_data(self, host, data, forward=None):
        if not self.enabled:
            return False
        elif forward is not None and forward is not self.ip_addr:
            return self.routing[forward].send(self, data, forward)
        self.data_queue.append(data)
        return True

    def get_data(self):
        if not self.enabled:
            raise DisabledHost("Host is not turned on.")

        try:
            return self.data_queue.pop(0)
        except IndexError:
            return False

    def is_linked(self, host=None, ip_addr=None):
        if not self.enabled:
            raise DisabledHost("Host is not turned on.")

        for link in self.links:
            if link.get_host(self) is host:
                return True
            elif link.get_host(self).ip_addr == ip_addr:
                return True

        return False

    def has_route_to(self, ip_addr):
        if ip_addr in self.routing:
            return True
        return False

    def send_data(self, ip_addr, packet):
        if isinstance(packet, basestring):
            packet = Packet(packet)

        if not isinstance(packet, Packet):
            raise TypeError("Packet must be of 'Packet' class or a string.")

        if ip_addr not in [host.ip_addr for host in self.network.hosts]:
            raise LookupError("Host must be on the same network.")

        if ip_addr in self.routing:
            __ = self.routing[ip_addr].send(host=self,
                                            data=packet,
                                            forward=ip_addr
            )

            return __


    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def invert(self):
        self.enabled ^= 1

    def __repr__(self):
        return "<NetworkDevice (IP address=%s)>" % self.ip_addr

    def discover(self, ip_addr, _ext=False):
        if ip_addr == self.ip_addr:
            raise InvalidDiscoveryHost("You cannot discover yourself.")

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
                    return False  # final method of discovering nodes
                self.routing[ip_addr] = link
                return link
        return False
