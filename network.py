"""
Contains all the hosts under a given external and local IP address.
"""

from exceptions import ExistingIP
from exceptions import HostNotFound
from exceptions import InvalidIP

from socket import error as socket_error
from socket import inet_aton


class Network(object):
    def __init__(self, label):
        self.gateway = None
        self.hosts = []
        self.label = label

    def __repr__(self):
        return "<kek at 0xkek>"

    def add_host(self, host):
        if host in self.hosts:
            raise ExistingIP("%s already exists in network." % host.ip_addr)
        elif host.ip_addr in [host_.ip_addr for host_ in self.hosts]:
            raise ExistingIP("%s already exists in network." % host.ip_addr)

        try:
            inet_aton(host.ip_addr)
        except socket_error:
            raise InvalidIP("%s is not a valid IP address." % host.ip_addr)

        if host.is_gateway:
            self.gateway = host

        self.hosts.append(host)
        return True

    def remove_host(self, host):
        if host not in self.hosts:
            raise HostNotFound("Host %s not found in network." % host.ip_addr)

        del self.hosts[self.hosts.index(host)]
        return True
