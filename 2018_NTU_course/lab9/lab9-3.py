import sys
import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.number import bytes_to_long

key = os.urandom(32)
registered = {}

def pad(s):
    p = 16 - len(s) % 16
    return s + bytes([p] * p)
def unpad(s):
    return s[:-s[-1]]

def pprint(s,n):
    for i in range(0,len(s),n):
        print(s[i:i+n])
    print()

def getAES(iv=None):
    if iv is None:
        iv = os.urandom(16)
    ctr = Counter.new(128, initial_value=bytes_to_long(iv))
    aes = AES.new(key, AES.MODE_CTR, counter=ctr)
    return aes, iv
# register
usr = 'AB'#input('[>] Username (hex): ')
usr = bytes.fromhex(usr)
mac = hashlib.md5(b'Crypto is fun' + usr + key).digest()
aes, iv = getAES()
token = (iv + aes.encrypt(usr + mac)).hex()
#====================================================
token = bytes.fromhex(token)
iv, token = token[:16], token[16:]
aes, iv = getAES(iv)
token = aes.decrypt(token)
usr, mac = token[:-16], token[-16:]
mac2 = hashlib.md5(b'Crypto is fun' + usr + key).digest()
print('mac : ',mac)
print('mac2: ',mac2)
from pwn import *   
def register(usr):
    r.sendlineafter('[>] ','register')
    r.sendlineafter('(hex): ',usr)
    token = r.recvuntil('\n\n').strip().split(b': ')[1]
    iv = token[:32]
    aes = token[32:]
    return iv,aes

def login(usr):
    r.sendlineafter('[>] ','login')
    r.sendlineafter('Token: ',usr)
    r.interactive()


r = remote('csie.ctf.tw',10136)
r.sendlineafter('[1~3]: ','3')
usr1 = '00'*51+'6F9C5091DF7A8D00FDC70C0553E0460D1622214BFC3D20CDC98EE7883B878F2ED56C3405099CF4625FE26A72534F2913AE7C7214EDD57A608AAB34EAE1FC8B67BA7B13B269FFF5E5A4E22F6D6FB37FFDD1936EC59B53CC0C24C9E586CC963DDD45683BBC9F9007A68669DD298C64761DCED0D9B37BA20B5166BCB8DD65919C89'
usr2 = '00'*51+'6F9C5091DF7A8D00FDC70C0553E0460D162221CBFC3D20CDC98EE7883B878F2ED56C3405099CF4625FE26A7253CF2913AE7C7214EDD57A608AAB346AE1FC8B67BA7B13B269FFF5E5A4E22F6D6FB37FFDD1936E459B53CC0C24C9E586CC963DDD45683BBC9F9007A68669DD298CE4751DCED0D9B37BA20B5166BCB85D65919C89'
prefix = b'Crypto is fun'.ljust(64,b'\x00').hex()
print(hashlib.md5(bytes.fromhex(prefix+usr1[102:])).digest())
print(hashlib.md5(bytes.fromhex(prefix+usr2[102:])).digest())
iv, aes= register(usr1)
l = len(usr1)
print('aes len:',   len(aes),l)
aes2 = hex(int(aes[:l],16)^int(usr1,16)^int(usr2,16))[2:].rjust(l,'0').encode('utf-8')+aes[l:]

## get flag
token2 = iv+aes2
login(token2)