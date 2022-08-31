import OpenOPC

import pywintypes

pywintypes.datetime = pywintypes.TimeType

opc = OpenOPC.client()
# 
servers = opc.servers()

# opc.connect('Kepware.KEPServerEX.V6')