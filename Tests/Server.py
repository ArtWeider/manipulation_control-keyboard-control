import socket
import time

HOST = '127.0.0.1'
PORT = 23

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("STARTED", HOST, PORT)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    print('test')
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024).decode('utf-8')
            print(data)
            time.sleep(1)
            conn.send(b'#')



