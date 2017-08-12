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

![Example topology](http://i.imgur.com/yEVclRz.png)

```python
from network.router import Router
from network.network import Network
from network.link import Link
from network.ethernet import Ethernet


network = Network("Network 1")

router1 = Router(
           network=network,
           ip_addr="0.0.0.1",
           is_gateway=False,
           mac_addr="00:00:00:00:00:00",
           label="Router 1"
           )

router2 = Router(
           network=network,
           ip_addr="0.0.0.2",
           is_gateway=False,
           mac_addr="00:00:00:00:00:01",
           label="Router 2",
           )

router3 = Router(
           network=network,
           ip_addr="0.0.0.3",
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

r2_data = Ethernet(
    dst_mac=router3.mac_addr,
    src_mac=router2.mac_addr,
    data="this data is from router 2",
)

r1_data = Ethernet(
    dst_mac=router3.mac_addr,
    src_mac=router1.mac_addr,
    data="this data is from router 1",
)

router2.discover("0.0.0.3")
router2.send_data("0.0.0.3", r2_data)
router1.send_data("0.0.0.3", r1_data)
print router3.data_queue
```

Which'd output:

```python
>>> [<Ethernet Packet (src=00:00:00:00:00:01) (dst=00:00:00:00:00:02) (data=this data is ...)>,
...  <Ethernet Packet (src=00:00:00:00:00:00) (dst=00:00:00:00:00:02) (data=this data is ...)>]
```  
