import json
import requests
requests.packages.urllib3.disable_warnings()

def get_interfaces():
    module="data/ietf-interfaces:interfaces"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    #print(json.dumps(resp.json(), indent=4))
    data_json = resp.json()

    if resp.status_code == 200:
        print('x')
        for key, valor in data_json.items():
            print(f'Nombre de la interface: {valor["interface"][0]["name"]}')
            print(f'Descripción de la interface: {valor["interface"][0]["description"]}')
            print(f'Status de la interface: {valor["interface"][0]["enabled"]}')
    else:
        print(f'Error al realizar la consulta del modulo{module}')    
def get_restconf_native():
    module="data/Cisco-IOS-XE-native:native"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        print(json.dumps(resp.json(), indent=4))
    else:
        print('Error al consumir la API para el modulo {module}')
        
def get_banner():
    module="data/Cisco-IOS-XE-native:native/banner/motd"
    resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 200:
        print(json.dumps(resp.json(), indent=4))
    else:
        print('Error al consumir la API para el modulo {module}')


def put_banner():
    banner = {
        "Cisco-IOS-XE-native:motd": {
        "banner": "## SOLO PERSONAL AUTORIZADO ## "
    }
    }

    module="data/Cisco-IOS-XE-native:native/banner/motd"
    resp = requests.put(f'{api_url}{module}', data=json.dumps(banner), auth=basicauth, headers=headers, verify=False)
    if resp.status_code == 204:
        print('Actualización exitosa')
    else:
        print(f'Error, no se puede realizar la actualización')

def post_loopback():
    dloopback = json.dumps({
  "ietf-interfaces:interface": {
    "name": "Loopback100",
    "description": "Configured by RESTCONF",
    "type": "iana-if-type:softwareLoopback",
    "enabled": True,
    "ietf-ip:ipv4": {
      "address": [
        {
          "ip": "172.16.100.1",
          "netmask": "255.255.255.0"
        }
      ]
    }
  }
})
    module = "data/ietf-interfaces:interfaces"
    resp = requests.post(f'{api_url}{module}', auth=basicauth, headers=headers,data=dloopback, verify=False)
    if resp.status_code == 201:
        print(f"Se insertó correctamente {dloopback}")
    else:
        print(f"Error al insertar el modulo {module}")



if __name__ == '__main__':
    #module:operations, data
    api_url = "https://192.168.56.104/restconf/"
    headers = {"Accept": "application/yang-data+json",
               "Content-type": "application/yang-data+json"
               }
    basicauth = ("cisco", "cisco123!")
    #get_interfaces()
    #get_restconf_native()
    #get_banner()
    #put_banner()
    post_loopback()