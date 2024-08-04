###############################################
#                  Group 14                   #
###############################################
#             Xin Wen (a1893343)              #
#           Yuhang Chen (a1914212)            #
###############################################

import rsa
import pickle
import json


def RsaEncrypt(str):
    (PubKey, PrivateKey) = rsa.newkeys(2048)
    content = str.encode('utf8')
    Encrypt_Str = rsa.encrypt(content, PubKey)
    return Encrypt_Str, PrivateKey
 
 
def RsaDecrypt(str, pk):
    Decrypt_Str = rsa.decrypt(str, pk)
    Decrypt_Str_1 = Decrypt_Str.decode('utf8')
    return Decrypt_Str_1
 
 
def SendMessage(SendData):
    (encryptdata, PrivateKey) = RsaEncrypt(SendData)
    Message = pickle.dumps([encryptdata, PrivateKey])
    return Message
 
 
def RecvMessage(Message):
    (recvdata, PrivateKey) = pickle.loads(Message)
    decryptdata = RsaDecrypt(recvdata, PrivateKey)
    return decryptdata


if __name__ == '__main__':
    Message = SendMessage("1")
    RecvMessage(Message)
 
 
