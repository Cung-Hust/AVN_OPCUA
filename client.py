from time import sleep
from opcua import Client
from pkg_resources import get_build_platform

# client = Client("opc.tcp://127.0.0.1:12345")
client = Client("opc.tcp://127.0.0.1:49320")

client.connect()

client.get_namespace_array()

objects = client.get_objects_node()

objects.get_children()

print(objects.get_children())

bulb = objects.get_children()[-2]

print(bulb)


a = bulb.get_children()[-1]

print(a)

print(a.get_browse_name())

b = a.get_children()[2]

print(b.get_value())

try:
    while True:
        print(b.get_value())
        # b.set_value(20)
        sleep(5)
finally:
    client.close_session()
