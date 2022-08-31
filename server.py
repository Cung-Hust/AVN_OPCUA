from http import server
from pydoc import tempfilepager
from time import sleep
import random
from opcua import Server
from pkg_resources import add_activation_listener

server = Server()

server.set_endpoint("opc.tcp://127.0.0.1:12345")

server.register_namespace("Room1")

objects = server.get_objects_node()

tempsens = objects.add_object('ns=2; s="TS1"', "Temperature Sensor 1")

tempsens.add_variable('ns=2; s="TS1_SerialNumber"',
                      "TS1 Serial Number", 12345678)

temp = tempsens.add_variable(
    'ns=2; s="TS1_Temperature"', "Temperature Temperature", 20)

bulb = objects.add_object(2, "Light Bulb")

state = bulb.add_variable(2, "State of Light Bulb", False)

state.set_writable()

temperature = 20.0
try:
    print("Start Server")
    server.start()
    print("Server Online")
    while True:
        temperature = random.uniform(-1, 1)
        temp.set_value(temperature)
        print("New Temperature: " + str(temp.get_value()))
        print("State of Light Bulb: " + str(state.get_value()))
        sleep(5)
finally:
    server.stop()
    print("Server Offline")
