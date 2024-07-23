from ncclient import manager
import xml.dom.minidom

#m = manager.connect(
#    host="192.168.56.104",
#    port=830,
#    username="cisco",
#    password="cisco123!",
#    hostkey_verify=False
#)

#print("#Supported Capabilities (YANG models):")
#for capability in m.server_capabilities:
#    print(capability)

# Retrieve the running configuration
#config = m.get_config(source="running").data_xml
#print(config)

#m.close_session()

netconf_filter = """
<filter>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native" />
</filter>
"""
netconf_loopback = """
<config>
 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  <interface>
   <Loopback>
    <name>1</name>
    <description>My NETCONF loopback</description>
    <ip>
     <address>
      <primary>
       <address>10.1.1.1</address>
       <mask>255.255.255.0</mask>
      </primary>
     </address>
    </ip>
   </Loopback>
  </interface>
 </native>
</config>
"""
with manager.connect(
    host="192.168.56.104",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
) as m:
    netconf_reply = m.edit_config(target="running", config=netconf_loopback)
    print(netconf_reply)
#as m:
   # netconf_reply = m.get_config(source="running", filter=netconf_filter)
   # print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

netconf_loopback = """
<config>
 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  <interface>
   <Loopback>
    <name>1</name>
    <description>My NETCONF loopback</description>
    <ip>
     <address>
      <primary>
       <address>10.1.1.1</address>
       <mask>255.255.255.0</mask>
      </primary>
     </address>
    </ip>
   </Loopback>
  </interface>
 </native>
</config>
"""
