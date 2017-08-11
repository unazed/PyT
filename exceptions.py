"""
Defines global exceptions.
"""


class ExistingIP(Exception):
    pass


class InvalidIP(Exception):
    pass


class InvalidDiscoveryHost(Exception):
    pass


class HostNotFound(Exception):
    pass


class DisabledHost(Exception):
    pass


class LinkFailure(Exception):
    pass


class MultipleGateways(Exception):
    pass


class TransmissionFailure(Exception):
    pass


class UnablePortConnection(Exception):
    pass


class DiscoveryFailure(Warning):
    pass
