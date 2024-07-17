import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Ruta del archivo JSON y XML
json_file_path = './data/infraestructura.json'
xml_file_path = './data/router.xml'

# Leer el archivo JSON
with open(json_file_path, 'r') as f:
    data = json.load(f)

# Convertir JSON a XML
root = ET.Element("root")

def create_xml_element(parent, key, value):
    key = key.replace(' ', '_')  # Reemplazar espacios por guiones bajos
    subelement = ET.SubElement(parent, key)
    subelement.text = str(value)

for key, value in data.items():
    item = ET.SubElement(root, key)
    for subitem in value:
        subelement = ET.SubElement(item, "element")
        for subkey, subvalue in subitem.items():
            create_xml_element(subelement, subkey, subvalue)

# Pretty print XML
xml_str = ET.tostring(root, 'utf-8')

try:
    parsed_xml = minidom.parseString(xml_str)
    pretty_xml_str = parsed_xml.toprettyxml(indent="  ")

    # Guardar XML en un archivo
    with open(xml_file_path, 'w') as f:
        f.write(pretty_xml_str)

except Exception as e:
    print(f"Error parsing XML: {e}")
    print(xml_str.decode('utf-8'))
    exit(1)

# Leer el archivo XML y extraer datos
tree = ET.parse(xml_file_path)
raiz = tree.getroot()

# Imprimir la raíz del XML
print(raiz)

# Extraer y mostrar los datos en la terminal
for router in raiz.findall('router/element'):
    model = router.find('model').text
    so = router.find('so').text
    router_type = router.find('type').text
    vendor = router.find('vendor').text
    print(f'Model: {model}\nSO: {so}\nType: {router_type}\nVendor: {vendor}\n')

for server in raiz.findall('server1/element'):
    linux_dist = server.find('linux_distribution').text
    name = server.find('name').text
    remote_con = server.find('remote_conection').text
    service = server.find('service').text
    print(f'Linux Distribution: {linux_dist}\nName: {name}\nRemote Connection: {remote_con}\nService: {service}\n')

for server in raiz.findall('server2/element'):
    linux_dist = server.find('linux_distribution').text
    name = server.find('name').text
    service1 = server.find('service1').text
    service2 = server.find('service2').text
    print(f'Linux Distribution: {linux_dist}\nName: {name}\nService 1: {service1}\nService 2: {service2}\n')

for server in raiz.findall('server3/element'):
    linux_dist = server.find('linux_distribution').text
    name = server.find('name').text
    service1 = server.find('service1').text
    service2 = server.find('service2').text
    print(f'Linux Distribution: {linux_dist}\nName: {name}\nService 1: {service1}\nService 2: {service2}\n')
