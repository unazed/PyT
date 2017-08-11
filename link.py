"""
Allows for 'physically' linking two hosts together
"""

from exceptions import LinkFailure
from exceptions import TransmissionFailure


class Link(object):
    def __init__(self, host1, host2):
        self.enabled = True

        self.map = {
            host1: host2,
            host2: host1
        }

        if not host1._link_create(self) or not host1._connect_port(host2):
            # The condition above is a bit ambiguous, may reconsider
            # repartitioning the conditions such that the ambiguity
            # is no more.

            raise LinkFailure("Failed creating link to %s." % host1.ip_addr)
        elif not host2._link_create(self) or not host2._connect_port(host1):
            raise LinkFailure("Failed creating link to %s." % host2.ip_addr)

        self.host1 = host1
        self.host2 = host2

    def get_host(self, host):
        "Get the opposite host."

        if not self.enabled:
            raise TransmissionFailure("The link is disabled and cannot perform"
                " any actions")

        return self.map[host]

    def send(self, host, data, forward=None):
        if not self.enabled:
            raise TransmissionFailure("The link is disabled and cannot perform"
                " any actions")
        elif not self.map[host]._link_queue_data(host, data, forward):
            return False
        return True

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def invert(self):
        self.enabled ^= 1
