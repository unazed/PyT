"""
Allows module scripts access range of utilities.
"""

from zlib import crc32


def eth_fcs(data):
  return crc32(data) % (1 << 32)    
