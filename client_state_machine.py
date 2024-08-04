###############################################
#                  Group 14                   #
###############################################
#             Xin Wen (a1893343)              #
#           Yuhang Chen (a1914212)            #
###############################################

from chat_utils import *
import json
import GUI
from encrypt import SendMessage


class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action": "connect", "target": peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with ' + self.peer + '\n'
            return True
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return False

    def disconnect(self):
        msg = json.dumps({"action": "disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def quit(self):
        msg = json.dumps({"action": "q"})
        mysend(self.s, msg)

    def proc(self, my_msg, peer_msg, file_name, login_name):
        self.out_msg = ''

        if self.state == S_LOGGEDIN:
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you later!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action": "time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in + '\n'

                elif my_msg == 'put':
                    mysend(self.s, json.dumps({"action": "put"}))
                    # time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += login_name + " put : " + file_name + '\n'

                elif my_msg == 'get':
                    mysend(self.s, json.dumps({"action": "get"}))
                    # time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += login_name + " get : " + file_name + '\n'

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action": "list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in + '\n'

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Start chatting!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action": "search", "target": term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                else:
                    self.out_msg = menu

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.state = S_CHATTING
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Start Chatting!\n\n'
                    self.out_msg += '------------------------------------\n'

        elif self.state == S_CHATTING:
            if len(my_msg) > 0:
                self.out_msg += "["+self.me+"]"+my_msg + '\n'
                # try:
                #     '''__import__('os').remove('text.txt')'''
                #     my_msg = str(eval(my_msg))
                # except:
                #     pass
                my_msg = str(my_msg)
                mysend(self.s, json.dumps({"action": "exchange", "from": "[" + self.me + "]", "message": my_msg}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
                # if my_msg == 'shit' or my_msg == 'damm':
                #     self.quit()
                #     self.out_msg += 'Rude words are not allowed!\n'
                #     self.state = S_OFFLINE
            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                
                if peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"
                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN
                    self.out_msg += 'Everyone left, you are alone.\n'
                else:
                    self.out_msg += peer_msg["from"] + peer_msg["message"] + '\n'
                self.out_msg = SendMessage(self.out_msg)
                print("Encrypted message：", self.out_msg)

            if self.state == S_LOGGEDIN:
                self.out_msg += menu

        else:
            self.out_msg += 'Goodbye\n'
            print_state(self.state)

        return self.out_msg

