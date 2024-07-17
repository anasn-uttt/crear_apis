import xml.etree.ElementTree as ET


tree = ET.parse('./data/router.xml')
raiz = tree.getroot()
print(raiz)

hostname = raiz.find('hostname').text
print(f'El nombre del router es {hostname}')

#interfaces = raiz.find('interfaces').text
#for interface in interfaces.findall('interface'):
#    nombre = interface.find('name').text
#    ip = interface.find('ip').text
#    submask = interface.find('subnet').text


