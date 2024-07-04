from flask import Flask, request, render_template,render_template, redirect, url_for
import json
#import paramiko
import time
import re
import requests
requests.packages.urllib3.disable_warnings()

app = Flask(__name__,static_folder='static')
@app.route('/dhcpool',methods=['GET', 'POST'])
def dhcpool():
    api_url = "https://192.168.56.104/restconf/"
    headers = {"Accept": "application/yang-data+json",
               "Content-type": "application/yang-data+json"
               }
    basicauth = ("cisco", "cisco123!")
    
    consulta = {}
    
   
    if request.method == 'POST' and request.form.get('action') == 'get':
        #print('la apppp¿pp¿')
    #print(api_url)
        module = "data/Cisco-IOS-XE-native:native/ip/dhcp"
        resp = requests.get(f'{api_url}{module}',  auth=basicauth, headers=headers, verify=False)
        consulta=resp.json()
        print(resp.json())
        
    if request.method == 'POST' and request.form.get('action') == 'agregarpool':   
        module = "data/Cisco-IOS-XE-native:native/ip/dhcp/"
        id=request.form.get('nameid-input')
        network=request.form.get('Network-input')
        mask=request.form.get('Mask-input')
        default=request.form.get('Default-input')
        dns=request.form.get('DNS-input')
        domain=request.form.get('Domain-input')
        
        
        """pool_config ={'Cisco-IOS-XE-native:dhcp': {'Cisco-IOS-XE-dhcp:pool': [
            {'id': id, 'default-router': {'default-router-list': [dafault]}, 
             'dns-server': {'dns-server-list': [dns]}, 
             'domain-name': domain, 
             'network': {'primary-network': {'number': network, 'mask': mask}}}]}}
        """
        pool_config = {
        "Cisco-IOS-XE-dhcp:pool": [
            {
                "id": id,
                "default-router": {
                    "default-router-list": [
                        default
                    ]
                },
                "dns-server": {
                    "dns-server-list": [
                        dns
                    ]
                },
                "domain-name": domain,
                "network": {
                    "primary-network": {
                        "number": network,
                        "mask": mask
                    }
                }
            }
        ]
    }
        
        """{
        "Cisco-IOS-XE-dhcp:pool": [
            {
                "id": id,
                "network": {
                    "primary": {
                        "address": network,
                        "mask": mask
                    }
                },
                "default-router": {
                    "default-router-list": [default]
                },
                "dns-server": {
                    "dns-server-list": [dns]
                },
                "domain-name": domain
            }
        ]
    }"""
        
        print(pool_config)
        print("Networksfgvbajvh aeocg repa")
        print(json.dumps(pool_config, indent=2))
        print("Enviando configuración del pool...")
        
        response = requests.post(f'{api_url}{module}', headers=headers, auth=basicauth, 
                             data=json.dumps(pool_config), verify=False)

   
        if response.status_code == 201:
            print("Nuevo pool DHCP agregado exitosamente")
        else:
            print(f"Error al agregar el nuevo pool DHCP: {response.status_code}")
            print(response.text)
            
    if request.method == 'POST' and request.form.get('action') == 'eliminarpool':   
        pool_id = request.form.get('idpoool-input')
        print(pool_id)
        module = "data/Cisco-IOS-XE-native:native/ip/dhcp/"
        resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
        
        config = resp.json()
        print(config)

        if 'Cisco-IOS-XE-dhcp:pool' in config['Cisco-IOS-XE-native:dhcp']:
            pools = config['Cisco-IOS-XE-native:dhcp']['Cisco-IOS-XE-dhcp:pool']

            # Filtra los pools para eliminar 'SubredD'
            updated_pools = [pool for pool in pools if pool['id'] != 'SubredD']

            # Actualiza la configuración con los pools restantes
            config['Cisco-IOS-XE-native:dhcp']['Cisco-IOS-XE-dhcp:pool'] = updated_pools

            # Realiza la solicitud PUT a la API para subir la configuración actualizada
            update_resp = requests.put(f'{api_url}{module}', auth=basicauth, headers=headers, json=config, verify=False)

            if update_resp.status_code == 204:
                print("Configuración actualizada exitosamente.")
            else:
                print(f"Error al actualizar la configuración: {update_resp.status_code} - {update_resp.text}")
            
            
        
    return render_template('dhcpool.html',consulta=consulta)
    
@app.route('/linevty',methods=['GET', 'POST'])
def linevty():
    api_url = "https://192.168.56.104/restconf/"
    headers = {"Accept": "application/yang-data+json",
               "Content-type": "application/yang-data+json"
               }
    basicauth = ("cisco", "cisco123!")
    
    consulta = {}
        
    if request.method == 'POST' and request.form.get('action') == 'get':
        module = "data/Cisco-IOS-XE-native:native/line/vty"
        #print('la apppp¿pp¿')
    #print(api_url)
        resp = requests.get(f'{api_url}{module}',  auth=basicauth, headers=headers, verify=False)
        consulta = resp.json()
        print(consulta)
        if resp.status_code == 200:
                consulta = resp.json()
                #print("Líneas VTY configuradas correctamente.")
        else:
                print(f'Error al configurar las líneas VTY')
                #print(resp.text)
            
    if request.method == 'POST' and request.form.get('action') == 'agregarline':   
        module = "data/Cisco-IOS-XE-native:native/line/vty"
        primera = int(request.form.get('name-input'))
        ultima= int(request.form.get('Ultima-input'))
        loginlocal = True if request.form.get('Loginlocal-input') == 'si' else False
        transport= request.form.get('Transporte-input')
        contra= request.form.get('contra-input')
        
        if loginlocal == True:
            loginlocal=[None]
        else:
             loginlocal=[]
        #print("vamos bieeen")
        #print(tipo,name,description,ip,mask)"""
        vty2 = {
            "Cisco-IOS-XE-native:vty": [
                {
                    "first": primera,
                    "last": ultima,
                    "login": {"local": loginlocal},
                    "password": {"secret": contra},
                    "transport": {"input": {"input": [transport]}}
                }
            ]
        }
        vty5={
            "Cisco-IOS-XE-native:vty": [
                {
                    "first": primera,
                    "last": ultima,
                    "login": {"local": [None] if not loginlocal else []},
                    "password": {"secret": contra},
                    "transport": {"input": {"input": [transport]}}
                }
            ]
        }
        vty = {
     "Cisco-IOS-XE-native:vty": [
            {
                "first": primera,
                "last": ultima,
                "login": {
                    "local": loginlocal
                },
                "password": {
                    "secret": contra
                },
                "transport": {
                    "input": {
                        "input": [transport]
                    }
                }
            } ]}
        
        
               #print(vty)
        
        #resp = requests.patch(f'{api_url}{module}', json=vty, auth=basicauth, headers=headers, verify=False)
        resp = requests.patch(f"{api_url}{module}", json=vty, auth=basicauth, headers=headers, verify=False)
        print(vty)  
        print(resp.status_code)
        
   
    if request.method == 'POST' and request.form.get('action') == 'eliminar':   
        
        
        primeraelim= int(request.form.get('primeraa-input'))
        segundaelim= int(request.form.get('ultimaa-input'))
        module = "data/Cisco-IOS-XE-native:native/line/vty"
        resp= requests.get(f'{api_url}{module}',  auth=basicauth, headers=headers, verify=False)
        vty_config = resp.json()
        for vty in vty_config.get('Cisco-IOS-XE-native:vty', []):
            print("sooooy",vty)
            print(vty.get('first'))
            print(vty.get('transport'))
            if vty.get('first') == primeraelim and vty.get('last') == segundaelim:
                updated_vty_config = {'Cisco-IOS-XE-native:vty': [{'first': primeraelim, 'last': segundaelim, 'login': {'local': [None]}, 
                                                            
                        'password': {'secret':""}, 'transport':vty.get('transport') }]}
                print("aisbebebe",updated_vty_config)
                response = requests.patch(f'{api_url}{module}', json=updated_vty_config, auth=basicauth, headers=headers, verify=False)
            
        # Enviar la solicitud PATCH para actualizar la configuración
        try:
            response = requests.patch(f'{api_url}{module}', json=updated_vty_config, auth=basicauth, headers=headers, verify=False)
            
            if response.status_code == 204:
                print("Comando enviado correctamente.")
            else:
                print(f"Error al enviar el comando. Código de estado: {response.status_code}")
                print("Respuesta:", response.text)  # Imprimir la respuesta para depuración
        except requests.exceptions.RequestException as e:
            print("Error en la solicitud:", e)

       
          
    
    return render_template('linevty.html', vty_list=consulta.get('Cisco-IOS-XE-native:vty', []))


@app.route('/interfacee',methods=['GET', 'POST'])
def interface():
    api_url = "https://192.168.56.104/restconf/"
    headers = {"Accept": "application/yang-data+json",
               "Content-type": "application/yang-data+json"
               }
    basicauth = ("cisco", "cisco123!")
    
    consulta = {}
        
    if request.method == 'POST' and request.form.get('action') == 'get':
        module="data/ietf-interfaces:interfaces"
        #print('la apppp¿pp¿')
    #print(api_url)
        resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)
        if resp.status_code == 200:
                consulta = resp.json()
                #consulta = "holaaaaaass"
                print(consulta)
        else:
            print(f'Error al consumir la API para el modulo {module}')
            
    if request.method == 'POST' and request.form.get('action') == 'agregar':   
        module="data/ietf-interfaces:interfaces"
        tipo = request.form.get('tipo-input')
        name= request.form.get('name-input')
        description= request.form.get('description-input')
        ip= request.form.get('ip-input')
        mask= request.form.get('mask-input')
        print("vamos bieeen")
        print(tipo,name,description,ip,mask)
        interfacee= json.dumps({
  "ietf-interfaces:interface": {
    "name": name,
    "description": description,
    "type": "iana-if-type:softwareLoopback",
    "enabled": True,
    "ietf-ip:ipv4": {
      "address": [
        {
          "ip": ip,
          "netmask": mask
        }
      ]
    }
  }
})
        
        
        resp=requests.post(f'{api_url}{module}',auth=basicauth,headers=headers,data=interfacee, verify=False)
        print(resp.status_code)
        if resp.status_code==201:
            print("swwwwwwwwwwwwwwwwwwwwwwwwwww3333i se oegoooo") 
   
    if request.method == 'POST' and request.form.get('action') == 'eliminar':   
        
        
        name= request.form.get('name-input')
        module="data/ietf-interfaces:interfaces/interface={}".format(name)
        
        print("vamos bieeen")
        interfacee= {}
        
        resp=requests.delete(f'{api_url}{module}',auth=basicauth,headers=headers,data=interfacee, verify=False)        
        print(resp.status_code)
        if resp.status_code==204:
            print("seliminadota y funadotaaaa") 
          
    
    return render_template('interfaces.html',consulta=consulta)

@app.route('/configure', methods=['GET', 'POST'])
def configure():
    api_url = "https://192.168.56.104/restconf/"
    headers = {"Accept": "application/yang-data+json",
               "Content-type": "application/yang-data+json"
               }
    basicauth = ("cisco", "cisco123!")
    consultaaaa = ""

    if request.method == 'POST' and request.form.get('action') == 'get':
        module = "data/Cisco-IOS-XE-native:native"
        #print('la apppp¿pp¿')
    #print(api_url)
        resp = requests.get(f'{api_url}{module}', auth=basicauth, headers=headers, verify=False)

        if resp.status_code == 200:
            consultaaaa = json.dumps(resp.json(), indent=4)
            #print("swwwwwwwwwwwwwwwwwwwwwwwwwww3333i se oegoooo")
        else:
            print(f'Error al consumir la API para el modulo {module}')
        
    
    
    return render_template('configure.html', api_url=api_url, headers=headers, basicauth=basicauth,consultaaaa=consultaaaa)
@app.route('/index')
def index():
    api_url = "https://192.168.56.104/restconf/"
    headers = {"Accept": "application/yang-data+json",
               "Content-type": "application/yang-data+json"
               }
    basicauth = ("cisco", "cisco123!")

    print('yaestamosenindex')
    print(f'API URL: {api_url}')
    
    #configure_url = url_for('configure', api_url=api_url, headers=json.dumps(headers), basicauth=json.dumps(basicauth))
    
    return render_template('index.html', api_url=api_url, headers=headers, basicauth=basicauth)

@app.route('/', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        #ip = request.form.get('ip')
        user = request.form.get('usuario')
        passs = request.form.get('contrasena')
        
        api_url = "https://192.168.56.104/restconf/"
        headers = {"Accept": "application/yang-data+json",
                "Content-type": "application/yang-data+json"
                }
        basicauth = (user, passs)
        module="data/Cisco-IOS-XE-native:native"
        resp=requests.get(f'{api_url}{module}',auth=basicauth,headers=headers, verify=False)
 
        if resp.status_code==200:
             print("yase pasosoooadjgalghoiaseg")
             
        else:
            print(f'Error al ingresar al router')   
         
        #return redirect(url_for('index', api_url=api_url, headers=json.dumps(headers), basicauth=json.dumps(basicauth)))     
        return redirect(url_for('index', api_url=api_url, headers=headers, basicauth=basicauth))
    
    
        
        
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)