###############################################
#                  Group 14                   #
###############################################
#             Xin Wen (a1893343)              #
#           Yuhang Chen (a1914212)            #
###############################################

import socket
import sys
from chat_utils import *
import client_state_machine as csm
from GUI import *

SERVER = ('127.0.0.1', 5555)
CHAT_PORT = 5555
FILE_SERVER = ('127.0.0.1', 5556)
FILE_PORT = 5556


class Client:
    def __init__(self, args):
        self.args = args

    def quit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def init_chat(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        svr = SERVER if self.args.d == None else (self.args.d, CHAT_PORT)
        self.socket.connect(svr)
        self.file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        svr = FILE_SERVER if self.args.d == None else (self.args.d, FILE_PORT)
        self.file_socket.connect(svr)
        self.sm = csm.ClientSM(self.socket)
        self.gui = GUI(self.send, self.recv, self.sm, self.socket, self.file_socket)

    def shutdown_chat(self):
        return

    def send(self, msg):
        mysend(self.socket, msg)

    def recv(self):
        return myrecv(self.socket)

    def run_chat(self):
        self.init_chat()
        self.gui.run()
        print("gui is off")
        self.quit()
