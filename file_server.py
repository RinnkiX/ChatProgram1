###############################################
#                  Group 14                   #
###############################################
#             Xin Wen (a1893343)              #
#           Yuhang Chen (a1914212)            #
###############################################

import threading
import queue
import json
import time
import os
import os.path
import socket
SERVER = ('127.0.0.1', 5556)
FILE_PORT = 5556


class FileServer(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        # self.setDaemon(True)
        self.ADDR = ('', port)
        # self.PORT = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.first = r'.\resources'
        os.chdir(self.first)
        # self.conn = None

    def tcp_connect(self, conn, addr):
        print(' Connected by: ', addr)
        
        while True:
            data = conn.recv(1024)
            data = data.decode()
            if data == 'quit':
                print('Disconnected from {0}'.format(addr))
                break
            order = data.split(' ')[0]
            self.recv_func(order, data, conn)
                
        conn.close()

    def sendList(self, conn):
        listdir = os.listdir(os.getcwd())
        listdir = json.dumps(listdir)
        conn.sendall(listdir.encode())

    def sendFile(self, message, conn):
        name = message.split()[1]
        fileName = r'./' + name
        try:
            with open(fileName, 'rb') as f:    
                while True:
                    a = f.read(1024)
                    if not a:
                        break
                    conn.send(a)
            time.sleep(0.1)
            conn.send('EOF'.encode())
        except:
            conn.send('File not found'.encode())
            conn.send('EOF'.encode())


    def recvFile(self, message, conn):
        name = message.split()[1]
        fileName = r'./' + name
        with open(fileName, 'wb') as f:
            while True:
                data = conn.recv(1024)
                if data == 'EOF'.encode():
                    break
                f.write(data)

    def cd(self, message, conn):
        message = message.split()[1]
        if message != 'same':
            f = r'./' + message
            os.chdir(f)
        path = os.getcwd().split('\\')
        for i in range(len(path)):
            if path[i] == 'resources':
                break
        pat = ''
        for j in range(i, len(path)):
            pat = pat + path[j] + ' '
        pat = '\\'.join(pat.split())
        if 'resources' not in path:
            f = r'./resources'
            os.chdir(f)
            pat = 'resources'
        conn.send(pat.encode())

    def recv_func(self, order, message, conn):
        if order == 'get':
            return self.sendFile(message, conn)
        elif order == 'put':
            return self.recvFile(message, conn)
        elif order == 'dir':
            return self.sendList(conn)
        elif order == 'cd':
            return self.cd(message, conn)

    def run(self):
        print('File server starts running...')
        self.s.bind(self.ADDR)
        self.s.listen(3)
        while True:
            conn, addr = self.s.accept()
            t = threading.Thread(target=self.tcp_connect, args=(conn, addr))
            t.start()
        self.s.close()
        
def main():
    fserver = FileServer(FILE_PORT)
    fserver.run()


if __name__ == '__main__':
    main()