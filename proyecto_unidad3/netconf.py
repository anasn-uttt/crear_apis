from ncclient import manager
from lxml import etree

m = manager.connect(
    host="192.168.56.1",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
)

#print("#Supported Capabilities (YANG models):")
#for capability in m.server_capabilities:
#    print(capability)

# Retrieve the running configuration
#config = m.get_config(source="running").data_xml
#print(config)
