# PyPT
(somewhat reimplementation of) packet tracer in python

A (during 11/08/2017) bare-bones implementation of [Packet Tracer](https://www.netacad.com/courses/packet-tracer-download/) (created by Cisco Systems) which at the final alpha development stage should implement several hardware recreations into the program for usage as nodes/network I/O devices such as:

- PC
- Laptop
- Smart phone
- Links
- Routers
- Switches

And more pretend items such as Networks which combine any form of physical hardware device into one local subnet, in the generic case the network would have a default gateway where all traffic is routed to if a route is not found within the local routing tables, and that router would (in the focus of the Internet topology) have an external address from the Network (such as a public IP address) for other networks to communicate with.

An example code-base would look something like this: (dated 11/08/2017)

```python
from network.router import Router
from network.network import Network
from network.link import Link
from network.ethernet import Ethernet


network = Network("Network 1")

router1 = Router(
           network=network,
           ip_addr="0.0.0.0",
           is_gateway=False,
           mac_addr="00:00:00:00:00:00",
           label="Router 1"
           )

router2 = Router(
           network=network,
           ip_addr="0.0.0.1",
           is_gateway=False,
           mac_addr="00:00:00:00:00:01",
           label="Router 2",
           )

router3 = Router(
           network=network,
           ip_addr="0.0.0.2",
           is_gateway=False,
           mac_addr="00:00:00:00:00:02",
           label="Router 3",
           )


Link(router2, router1)
Link(router3, router1)

#    [router 2]    [router3]
#         \          /
#          \        /
#          [router1]

data = Ethernet(
    dst_mac="00:00:00:00:00:02",
    src_mac="00:00:00:00:00:01",
    type_="\x08\x00",
    data="",
    crc="test"
)

assert router1.is_linked(router2), "r1 -!-> r2"
assert router1.is_linked(router3), "r1 -!-> r3"
assert router2.is_linked(router1), "r2 -!-> r1"
assert router3.is_linked(router1), "r3 -!-> r1"
assert not router2.send_data("0.0.0.2", data)
assert router1.send_data("0.0.0.1", data)
assert router1.send_data("0.0.0.2", data)
print(router2.data_queue)
print(router3.data_queue)
```
