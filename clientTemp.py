from time import sleep
from opcua import Client, ua

# client = Client("opc.tcp://127.0.0.1:12345")
client = Client("opc.tcp://127.0.0.1:49320")

client.connect()

client.get_namespace_array()

objects = client.get_objects_node()

objects.get_children()

print(objects.get_children())

bulb = objects.get_children()[-4]

print(bulb)

print(bulb.get_children())

a = bulb.get_children()[-1]

print(a)

print(a.get_browse_name())

print(a.get_children())

b = a.get_children()[2]
d = a.get_children()[4]

# print(b.set_value(30))

# c = client.get_node("ns=2;i=13")

# print(c.get_children())
try:
    while True:
        print(b.get_value())
        sleep(2)
        print(d.get_value())
        # d.set_value(21.05)
        sleep(2)
        # c.set_value(ua.AttributeIds.Value, 20.0)
finally:
    client.close_session()
