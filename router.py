"""
Routes data between subnets and networks.
"""

from networkdevice import NetworkDevice
from ethernet import Ethernet
from packet import Packet
from exceptions import DiscoveryFailure
from warnings import warn

from threading import Thread


class Router(NetworkDevice):
    def __init__(self, **kwargs):
        if not 'nports' in kwargs:
            kwargs['nports'] = 4
        super(Router, self).__init__(**kwargs)
        self._thread_running = False
        self._kill_thread = False

    def ping(self, host):
        if not self.discover(host.ip_addr):
            warn("Failed to discover host", DiscoveryFailure)
            return False

        eth_packet = Ethernet(host.mac_addr, self.mac_addr, "\x08\x00", "PING",
                              "good")
        eth_packet = Packet(eth_packet)
        self.send_data(host.ip_addr, eth_packet)
        return True
