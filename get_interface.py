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
        
if __name__ == '__main__':
    #module:operations, data
    api_url = "https://192.168.56.104/restconf/"
    headers = {"Accept": "application/yang-data+json",
               "Content-type": "application/yang-data+json"
               }
    basicauth = ("cisco", "cisco123!")
    get_interfaces()

    