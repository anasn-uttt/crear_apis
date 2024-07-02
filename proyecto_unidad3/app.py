from flask import Flask, request, render_template,render_template, redirect, url_for
import json
#import paramiko
import time
import re
import requests
requests.packages.urllib3.disable_warnings()

app = Flask(__name__,static_folder='static')

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