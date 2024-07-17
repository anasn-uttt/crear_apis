import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(hostname='192.168.10.20', port=22, username='admin1',password='huawei')

cmd = ssh.invoke_shell()
cmd.send('screen-length 0 temporary\n')
cmd.send('dis cu\n')
cmd.send("system \n")

for n in range(10, 21):
    print("Creating Vlan" + str(n))
    cmd.send("vlan " + str(n) + "\n")
    cmd.send("description Python Vlan" + str(n) + "\n")
    time.sleep(3)
    
    
#cmd.send('system \n')
#cmd.send('vlan 20\n')
#time.sleep(3)

show_res= cmd.recv(999999).decode()
print(show_res)
ssh.close()