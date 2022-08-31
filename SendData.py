#!/usr/bin/python3

import sys
import time
sys.path.insert(0, "..")

from opcua import Client, ua

if __name__ == "__main__":

    # client = Client("opc.tcp://192.168.0.5:49320")
    client = Client("opc.tcp://CUNG:49320")
    try:
        client.connect()

        # get a specific node knowing its node id
        var = client.get_node("ns=2;s=Channel2.Device1.OnlineState")
        #var = client.get_node("ns=4;s=MAIN.ConditionAutoClose.sGiveHour")

        print(var)
        k = var.get_data_value() # get value of node as a DataValue object
        print(k)
        j = 0
        while True:
            i = var.get_value() # get value of node as a python builtin
            print(i)
            time.sleep(3)
            j = j + 1.0
            data = "Hello " + str(j)
            # var.set_attribute(ua.AttributeIds.Value, ua.DataValue(20.0))
            dv = ua.DataValue(ua.Variant(data, ua.VariantType.String))
            var.set_value(dv)

        #var.set_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        # var.set_value(20) # set node value using implicit data type

    finally:
        client.disconnect()