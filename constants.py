"""
Defines constants to be used over the modules.
"""


IP_CLASSES = {
    "A": (1, 126),
    "B": (128, 191),
    "C": (192, 223),
    "D": (224, 239),
    "E": (240, 255)
}

PRIVATE_IP_CLASSES = {
    "24": ("10.0.0.0", "10.255.255.255"),
    "20": ("172.16.0.0", "172.31.255.255"),
    "16": ("192.168.0.0", "192.168.255.255"),
}

MAX_PACKET_SIZE = 1518  # bytes, and this only defines the maximum Ethernet size
                        # with-out fragmentation
MIN_PACKET_SIZE = 18  # again Ethernet-based.
