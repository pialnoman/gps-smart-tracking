import socket
import threading
from datetime import time
from timeit import Timer

HOST, PORT = "localhost", 8100
# data = bytes('\x78\x78\x0d\x01\x08\x68\x00\x30\x32\x43\x34\x63\x00\x17\xcd\x12\x0d\x0a', encoding='utf-8')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
datas = bytes('', encoding='utf-8')
received = bytes('', encoding='utf-8')


def send_data(data):
    datas = data
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(data)


try:
    while True:
        t1 = Timer(2, send_data(bytes('\x78\x78\x0d\x01\x08\x68\x00\x30\x32\x43\x34\x63\x00\x17\xcd\x12\x0d\x0a', encoding='utf-8')))
        t2 = Timer(10, send_data(bytes('\x78\x78\x1f\x12\x14\x02\x1a\x10\x0f\x23\xc7\x02\x8d\x84\x97\x09\xb3\x51\x8d\x00\x14\x71\x01\xd6\x00\x52\x18\x00\x2b\x86\x00\x23\xf8\xf6\x0d\x0a', encoding='utf-8')))
        t1.start()
        t2.start()

        # while True:
        #     ticker = threading.Event()
        #     while not ticker.wait(10):
        #         sock.sendall(bytes('\x78\x78\x0d\x01\x08\x68\x00\x30\x32\x43\x34\x63\x00\x17\xcd\x12\x0d\x0a', encoding='utf-8'))
        #
        #     ticker2 = threading.Event()
        #     while not ticker2.wait(61):
        #         sock.sendall(bytes('\x78\x78\x1f\x12\x14\x02\x1a\x10\x0f\x23\xc7\x02\x8d\x84\x97\x09\xb3\x51\x8d\x00\x14\x71\x01\xd6\x00\x52\x18\x00\x2b\x86\x00\x23\xf8\xf6\x0d\x0a', encoding='utf-8'))

        # Receive data from the server and shut down
        received = sock.recv(76)
except Exception as e:
    print(e)
    # sock.close()

print("Sent:     {}".format(datas))
print("Received: {}".format(received))
