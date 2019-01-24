# break broken CBC_MAC
import sys
import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.number import bytes_to_long

def pad(s):
    p = 16 - len(s) % 16
    return s + bytes([p] * p)
def unpad(s):
    return s[:-s[-1]]

def pprint(s,n):
    for i in range(0,len(s),n):
        print(s[i:i+n])
    print()
key = os.urandom(32)
iv = os.urandom(16)

def CBC_MAC2(s):
    aes = AES.new(key, AES.MODE_CBC, iv)
    rawaes = aes.encrypt(pad(s)+b'\x00'*16)
    mac = rawaes[-16:].hex().rjust(32,'0')
    return mac


def CBC_MAC(s):
    s=bytes.fromhex(s)
    aes = AES.new(key, AES.MODE_CBC, iv)
    print('hex(s):')
    pprint(pad(s).hex(),32)
    rawaes = aes.encrypt(pad(s))
    rawmac = rawaes[-16:]
    print('aes:')
    pprint(rawaes.hex(),32)
    # Encrypt-last-block
    aes = AES.new(key, AES.MODE_ECB)
    mac = aes.encrypt(rawmac).hex().rjust(32, '0')

    print('mac:')
    pprint(mac,32)
    return mac


import binascii
c2 = CBC_MAC('AA')
CBC_MAC('AA'+'0F'*15+'00'*16+c2)
# we know \xAA * + '\x0f' * 15 + '\x00' * 16 (c2)
# m3^c2 controlable, we let it to bet zero.
print('stage 2')
c2 = CBC_MAC('AB')
CBC_MAC('AB'+'0F'*15+'00'*16+c2)
from pwn import *
r = remote('csie.ctf.tw',10136)
r.send('2\n')
def submit(msg1,msg2):
    r.sendlineafter('[>] First (hex): ',msg1)
    r.sendlineafter('[>] Second (hex): ',msg2)
    ret = r.recv().strip()
    return ret

mac1, _, mac2 =  submit('AA','AB').decode().split()[3:6]
msg1 = 'AA'+'0F'*15+'00'*16+mac1
msg2 = 'AB'+'0F'*15+'00'*16+mac2
print(submit(msg1,msg2).decode())
