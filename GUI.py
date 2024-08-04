#!/usr/bin/env python3

# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import messagebox
from chat_utils import *
import json
from PIL import Image, ImageTk
import socket
import requests
from tkinter import filedialog
import os
import getpass
import hashlib
import random
from encrypt import RecvMessage
from chat_group import Group


# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s, file_socket):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""

        self.file_socket = file_socket
        self.file_name = ""
        
        self.ldm1 = Image.open('facepalm.png')
        self.memes1 = ImageTk.PhotoImage(self.ldm1)
        
        self.ldm2 = Image.open('smart.png')
        self.memes2 = ImageTk.PhotoImage(self.ldm2)
        
        self.ldm3 = Image.open('smirk.png')
        self.memes3 = ImageTk.PhotoImage(self.ldm3)
        
        self.ldm4 = Image.open('concerned.png')
        self.memes4 = ImageTk.PhotoImage(self.ldm4)
        
        self.memesdic = {
            "1": self.memes1,
            "2": self.memes2,
            "3": self.memes3,
            "4": self.memes4,
            }

        self.countpassword = 0

    def login(self):
        self.flag = False
        self.login_name = ''

        # login window
        self.login = Toplevel()
        self.login.title("Login")
        self.login.geometry('450x300')
        self.pls = Label(self.login, 
                         text="Please login",
                         font="Helvetica 14 bold")
        self.pls.place(x=60, y=65)
        
        # Label - username / password
        self.labelName = Label(self.login,
                               text="Username: ",
                               font="Helvetica 12")
        self.labelName.place(x=90, y=130)
        self.labelPwd = Label(self.login, 
                              text="Password: ",
                              font="Helvetica 12")
        self.labelPwd.place(x=90, y=170)
        
        # entry box - username / password
        self.var_usr_name = StringVar()
        self.entry_usr_name = Entry(self.login, textvariable=self.var_usr_name)
        self.entry_usr_name.place(x=180, y=130)
        self.var_usr_pwd = StringVar()
        self.entry_usr_pwd = Entry(self.login, textvariable=self.var_usr_pwd, show='*')
        self.entry_usr_pwd.place(x=180, y=170)
        
        # button - login / registration / quit
        self.bt_login = Button(self.login, text='Login', command=lambda: self.usr_log_in(self.var_usr_name.get(), self.var_usr_pwd.get()))
        self.bt_login.place(x=110, y=230)
        self.bt_logreg = Button(self.login, text='Registration', command=lambda: self.usr_sign_up())
        self.bt_logreg.place(x=180, y=230)
        self.bt_logquit = Button(self.login, text='Quit', command=lambda: self.usr_sign_quit())
        self.bt_logquit.place(x=290, y=230)
        
        self.Window.mainloop()

    def hash_password(self, password):
        h = hashlib.sha256()
        h.update(password.encode())
        return h.hexdigest()

    # login
    def usr_log_in(self, var_usr_name, var_usr_pwd):
        usr_name = var_usr_name
        usr_pwd = var_usr_pwd
        accounts = {}
        file_name = "usr_info.txt"

        with open(file_name, "r") as file:
            for line in file:
                username, password = line.strip().split("::")
                accounts[username] = password

        if usr_name == '' or usr_pwd == '':
            messagebox.showerror(message='Username or password is empty.')

        if usr_name in accounts.keys():
            hashed_password = self.hash_password(usr_pwd)
            if hashed_password == accounts[usr_name]:
                messagebox.showinfo(message='Welcome '+usr_name+'!')
                self.flag = True
                self.login_name = usr_name
                self.gopage = Toplevel(self.login)
                self.gopage.title("CHATROOM")
                self.gopage.geometry('450x300')
                self.wel = Label(self.gopage,
                                 text="Welcome to Chatroom!",
                                 font="Helvetica 14 bold")
                self.wel.place(x=60, y=65)
                self.go = Button(self.gopage,
                                 text="CONTINUE",
                                 font="Helvetica 14 bold",
                                 command=lambda: self.goAhead(self.login_name))
                self.go.place(x=80, y=120)
            elif self.countpassword == 4:
                messagebox.showerror(message='You have reached login limit')
                self.Window.after(3000, self.Window.destroy)
            else:
                messagebox.showerror(message='Incorrect password.')
                self.countpassword += 1

        else:
            is_signup = messagebox.askyesno(message='You have not registered yet, would you like to register now?')
            if is_signup:
                self.usr_sign_up()

    # Register
    def usr_sign_up(self):
        def signtoreg():
            nn = var_new_name.get()
            np = var_new_pwd.get()
            npf = var_new_pwd_confirm.get()
            file_name = "usr_info.txt"
            with open(file_name, "r") as f:
                for line in f:
                    account, _ = line.strip().split("::")
                    if account == nn:
                        messagebox.showerror('Error!', 'Username already exists.')
                    elif np == '' or nn == '':
                        messagebox.showerror('Error!', 'Username or password is empty.')
                    elif np != npf:
                        messagebox.showerror('Error!', 'Inconsistent passwords.')
            with open(file_name, "a") as f:
                hashed_password = self.hash_password(np)
                f.write(f"{nn}::{hashed_password}\n")
                messagebox.showinfo('Registered successfully!', 'Welcome!')
                self.flag = True
                self.login_name = nn
                window_sign_up.destroy()
                self.gopage = Toplevel(self.login)
                self.gopage.title("CHATROOM")
                self.gopage.geometry('450x300')
                self.wel = Label(self.gopage, 
                                 text="Welcome to Chatroom!",
                                 font="Helvetica 14 bold")
                self.wel.place(x=60, y=65)
                self.go = Button(self.gopage,
                                 text="CONTINUE",
                                 font="Helvetica 14 bold",
                                 command=lambda: self.goAhead(self.login_name))
                self.go.place(x=80, y=120)
                
        # new register interface
        window_sign_up = Toplevel(self.login)
        window_sign_up.geometry('350x200')
        window_sign_up.title('Registration')
        # username
        var_new_name = StringVar()
        new_name = Label(window_sign_up, text = 'Username：').place(x=10,y=10)
        enter_new_name = Entry(window_sign_up, textvariable = var_new_name).place(x=150,y=10)
        # password
        var_new_pwd = StringVar()
        new_pwd = Label(window_sign_up, text = 'Password：').place(x=10,y=50)
        enter_new_pwd = Entry(window_sign_up, textvariable = var_new_pwd, show = '*').place(x=150,y=50)    
        # password again
        var_new_pwd_confirm = StringVar()
        new_pwd_confirm = Label(window_sign_up, text = 'Confirm Password：').place(x=10,y=90)
        enter_new_pwd_confirm = Entry(window_sign_up, textvariable = var_new_pwd_confirm, show = '*').place(x=150,y=90)
        # confirm register
        bt_confirm_sign_up = Button(window_sign_up, text='Complete Registration', command=signtoreg)
        bt_confirm_sign_up.place(x=150, y=130)
        
        window_sign_up.mainloop()

    # Quit
    def usr_sign_quit(self):
        self.login.destroy()
    
    def goAhead(self, name):
        if len(name) > 0:
            msg = json.dumps({"action": "login", "name": name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.textCons.config(state=NORMAL)
                self.textCons.insert(END, menu +"\n\n")      
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)

            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()
  
    # The main layout of the chat
    def layout(self, name):
        self.name = name
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=470,
                              height=550,
                              bg="#331100")
        self.labelHead = Label(self.Window,
                               bg="#331100",
                               fg="#FFEAE6",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)
          
        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#FFEAE6")
          
        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)
        

        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#331100",
                             fg="#FFEAE6",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)
         
        self.textCons.place(relheight=0.662,
                            relwidth=1,
                            rely=0.08)

        self.labelBottom = Label(self.Window,
                                 bg="#FFEAE6",
                                 height=80)
          
        self.labelBottom.place(relwidth=1,
                               rely=0.745)

        # entry message
        self.entryMsg = Entry(self.labelBottom,
                              bg="#331100",
                              fg="#FFEAE6",
                              font="Helvetica 13")

        self.entryMsg.place(relwidth=0.8,
                            height=32,
                            y=43,
                            relx=0.005)
          
        self.entryMsg.focus()
        
        # send button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#FFEAE6",
                                command=lambda: self.sendButton(self.entryMsg.get()))
          
        self.buttonMsg.place(relx=0.77995,
                             y=43,
                             height=32,
                             relwidth=0.22)
          
        self.textCons.config(cursor="arrow")
        
        # location button
        self.buttonLoc = Button(self.Window,
                                text="Location",
                                font="Helvetica 10 bold",
                                bg="#FFEAE6",
                                command=lambda: self.locButton())
        self.buttonLoc.place(x=50, y=415)

        # memes button
        self.buttonMemes = Button(self.Window,
                                  text="Memes",
                                  font="Helvetica 10 bold",
                                  bg="#FFEAE6",
                                  command=lambda: self.memesButton())
        self.buttonMemes.place(x=270, y=415)

        # time button
        self.buttonTime = Button(self.Window,
                                 text="Time",
                                 font="Helvetica 10 bold",
                                 bg="#FFEAE6",
                                 command=lambda: self.timeButton())
        self.buttonTime.place(x=0, y=415)
        
        # list users button
        self.buttonUser = Button(self.Window,
                                 text="List Users",
                                 font="Helvetica 10 bold",
                                 bg="#FFEAE6",
                                 command=lambda: self.listUsers())
        self.buttonUser.place(x=120, y=415)

        # connect button
        self.buttonCon =Button(self.Window,
                               text="Connect",
                               font="Helvetica 10 bold",
                               bg="#FFEAE6",
                               command=lambda: self.chatButton())
        self.buttonCon.place(x=200, y=415)

        # send file button
        self.buttonMemes = Button(self.Window,
                                  text="Files",
                                  font="Helvetica 10 bold",
                                  bg="#FFEAE6",
                                  command=lambda: self.fileButton())
        self.buttonMemes.place(x=340, y=415)

        # leave button
        self.buttonLve = Button(self.Window,
                                text="Leave",
                                font="Helvetica 10 bold",
                                bg="#FFEAE6",
                                command=lambda: self.leaveButton())
        self.buttonLve.place(x=400, y=415)

        # download button
        self.buttonDow = Button(self.Window,
                                text="Download",
                                font="Helvetica 10 bold",
                                bg="#FFEAE6",
                                command=lambda: self.downButton())
        self.buttonDow.place(x=0, y=500)

        # upload button
        self.buttonFile = Button(self.Window,
                                 text="Upload",
                                 font="Helvetica 10 bold",
                                 bg="#FFEAE6",
                                 command=lambda: self.sendFile())
        self.buttonFile.place(x=100, y=500)

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
          
        # place the scroll bar 
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)
          
        scrollbar.config(command=self.textCons.yview)
          
        self.textCons.config(state=DISABLED)
    
    # memes function
    def memesButton(self):
        self.memesBox = Frame(self.Window, bg="#FFEAE6")
        self.memesBox.place(width=200, height=260, x=150, y=140)
        
        self.me1=Button(self.memesBox, text='Memes 1', command=self.Meme_1, image=self.memes1)
        self.me1.place(x=10, y=40)
        
        self.me2=Button(self.memesBox, text='Memes 2', command=self.Meme_2, image=self.memes2)
        self.me2.place(x=110, y=40)
        
        self.me3=Button(self.memesBox, text='Memes 3', command=self.Meme_3, image=self.memes3)
        self.me3.place(x=10, y=150)
        
        self.me4=Button(self.memesBox, text='Memes 4', command=self.Meme_4, image=self.memes4)
        self.me4.place(x=110, y=150)
        
        self.levme=Button(self.memesBox, text='OK', command=self.memesDone)
        self.levme.place(x=0, y=0, width=30, height=30)
    
    def Meme_1(self):
        self.my_msg = 'MEMES 1'
    
    def Meme_2(self):
        self.my_msg = 'MEMES 2'
        
    def Meme_3(self):
        self.my_msg = 'MEMES 3'
        
    def Meme_4(self):
        self.my_msg = 'MEMES 4'
    
    def memesDone(self):
        self.memesBox.destroy()

    # location button
    def locButton(self):
        # Get the public IP address
        ip_response = requests.get('https://httpbin.org/ip')
        myip = ip_response.json()['origin']

        # Get location data for the public IP address
        url = f'http://ip-api.com/json/{myip}'
        response2 = requests.get(url)
        strpp = response2.json()

        locmsg = "****************************************\n"
        locmsg += f"Your IP: {strpp.get('query')}\n"
        locmsg += f"Country: {strpp.get('country')}\n"
        locmsg += f"City: {strpp.get('city')}\n"
        locmsg += f"Longitude: {strpp.get('lon')}\n"
        locmsg += f"Latitude: {strpp.get('lat')}\n"
        locmsg += "Data Source: <www.ip-api.com>\n"
        locmsg += "****************************************"

        self.locBox = Frame(self.Window, bg="#FFEAE6")
        self.locBox.place(width=200, height=200, x=200, y=200)
        self.location = Label(self.locBox, text=locmsg, font="Helvetica 10 bold")
        self.location.place(width=200,
                            height=60, x=0,
                            y=40)
        self.recloc=Button(self.locBox, text='OK', command=self.locationDone)
        self.recloc.place(x=0, y=0, width=30, height=30)
        
    def locationDone(self):
        self.locBox.destroy()
    
    # time function
    def timeButton(self):
        self.my_msg = 'time'
    
    # list users function
    def listUsers(self):
        self.my_msg = 'who'
    
    # leave function
    def leaveButton(self):
        self.my_msg = 'q'
        self.Window.destroy()
    
    # chat function
    def chatButton(self):
        self.peerMatch = Frame(self.Window, bg='#FFEAE6')
        self.peerMatch.place(width=100, height=100, x=250, y=300)
        self.peerName = Entry(self.peerMatch,
                              bg="#331100",
                              fg="#FFEAE6",
                              font="Helvetica 13")
        self.peerName.place(width=90,
                            height=35, x=0,
                            y=60)
        self.c=Button(self.peerMatch, text='Connect', command=self.connectionDone)
        self.c.place(x=0, y=0, width=65, height=30)
        self.levc=Button(self.peerMatch, text='OK', command=self.directchatDone)
        self.levc.place(x=65, y=0, width=30, height=30)

    ### send file function
    def fileButton(self):
        self.peerMatch = Frame(self.Window, bg='#FFEAE6')
        self.peerMatch.place(width=100, height=100, x=250, y=300)
        self.fileNameEntry = Entry(self.peerMatch,
                                   bg="#331100",
                                   fg="#FFEAE6",
                                   font="Helvetica 13")
        self.fileNameEntry.place(width=90,
                                 height=35,
                                 x=0,
                                 y=60)
        self.c = Button(self.peerMatch, text='Transfer', command=self.sendFile1)
        self.c.place(x=0, y=0, width=65, height=30)
        self.levc = Button(self.peerMatch, text='OK', command=self.directchatDone)
        self.levc.place(x=65, y=0, width=30, height=30)

    def downButton(self):
        self.peerMatch = Frame(self.Window, bg='#FFEAE6')
        self.peerMatch.place(width=100, height=100, x=250, y=300)

        self.peerName = Entry(self.peerMatch,
                              bg="#331100",
                              fg="#FFEAE6",
                              font="Helvetica 13")
        self.peerName.place(width=90,
                            height=35, x=0,
                            y=60)
        self.c = Button(self.peerMatch, text='Download', command=self.fileGet)
        self.c.place(x=0, y=0, width=65, height=30)
        self.levc = Button(self.peerMatch, text='OK', command=self.directchatDone)
        self.levc.place(x=65, y=0, width=30, height=30)

    def sendFile1(self):
        file_path = self.fileNameEntry.get()
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                file_content = file.read()
                self.my_msg = file_path + '\n' + file_content
                self.peerMatch.destroy()
        else:
            self.my_msg = "File does not exist"

    def sendFile(self):
        fileName = filedialog.askopenfilename(title='Select upload file')
        if fileName:
            self.filePut(fileName)

    def filePut(self, fileName):
        print(fileName)
        name = fileName.split('/')[-1]
        print(name)
        self.file_name = name
        self.my_msg = 'put'
        message = 'put ' + name
        self.file_socket.send(message.encode())
        time.sleep(0.1)
        print('Start uploading file!')
        print('Waiting.......')
        with open(fileName, 'rb') as f:
            while True:
                a = f.read(1024)
                if not a:
                    break
                self.file_socket.send(a)
            time.sleep(0.1)
            self.file_socket.send('EOF'.encode())
            print('Upload completed')
        time.sleep(0.1)

    def fileGet(self):
        pname = self.peerName.get()
        message = 'get ' + pname
        self.my_msg = 'get'
        self.file_name = pname
        self.file_socket.send(message.encode())
        fileName = '.\\Client_file_cache\\' + pname
        print('Start downloading image!')
        print('Waiting.......')
        with open(fileName, 'wb') as f:
            while True:
                data = self.file_socket.recv(1024)
                if data == 'EOF'.encode():
                    print('Download completed!')
                    break
                f.write(data)
        time.sleep(0.1)

    def directchatDone(self):
        self.peerMatch.destroy()
        
    def connectionDone(self):
        pname = self.peerName.get()
        self.my_msg = 'c' + pname
        self.peerMatch.destroy()

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.my_msg = msg
        self.entryMsg.delete(0, END)

        # if msg.startswith("/secret"):
        #     self.textCons.config(state=NORMAL)
        #     self.textCons.insert(END, "Accessing secret data...\n")
        #     self.textCons.insert(END, "THIS IS THE SECRET LINE!\n")
        #     self.textCons.config(state=DISABLED)
        #     self.textCons.see(END)
        #     command = msg.split(" ")[1]
        #     if command == "shutdown":
        #         self.textCons.config(state=NORMAL)
        #         self.textCons.insert(END, "Server is shutting down...\n")
        #         self.textCons.config(state=DISABLED)
        #         self.textCons.see(END)
        #         # Simulate server shutdown
        #         self.Window.after(5000, self.Window.destroy)

    def proc(self):
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                self.system_msg = ""
                return_msg = self.sm.proc(self.my_msg, peer_msg, self.file_name, self.login_name)
                try:
                    self.system_msg += RecvMessage(return_msg)
                    print("Decrypted message:" + self.system_msg)
                except:
                    self.system_msg += return_msg
                # self.system_msg += self.sm.proc(self.my_msg, peer_msg,self.file_name,self.login_name)
                self.my_msg = ""
                self.textCons.config(state=NORMAL)
                self.textCons.insert(END, self.system_msg + "\n")
                if 'MEMES' in self.system_msg:
                    memes_index = self.system_msg[-2]
                    self.textCons.image_create(END, image=self.memesdic[memes_index])
                    self.textCons.insert(END, "\n")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)

    def run(self):
        self.login()


# create a GUI class object
if __name__ == "__main__": 
    g = GUI()
