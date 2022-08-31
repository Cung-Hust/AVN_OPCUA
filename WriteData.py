#!/usr/bin/python3

import sys
import time
import random

from torch import randint
sys.path.insert(0, "..")

from opcua import Client, ua

if __name__ == "__main__":

    client = Client("opc.tcp://CUNG:49320")
    try:
        client.connect()
        while True:
            for i in range(1, 11):
                index = '{0:03}'.format(i)
                # print(index)
                var = client.get_node(f"ns=2;s=Channel2.Device1.KWh-{index}")
                # print(var)
                data = random.randint(100, 1000)
                print(data)
                dv = ua.DataValue(ua.Variant(data, ua.VariantType.Float))
                var.set_value(dv)
            time.sleep(5)
    finally:
        client.disconnect()