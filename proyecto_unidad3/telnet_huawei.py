import telnetlib
import time

host = '192.168.10.20' 
password = 'Huawei@123'

tn =telnetlib.Telnet (host)


tn.read_until (b"Password: ") 
tn.write(password.encode('ascii') + "\n") 
tn.write(b'display cu \n') 
time.sleep(1)

print(tn.read_very_eager().decode('ascii'))
tn.close()