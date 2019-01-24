from pwn import *
r = remote('csie.ctf.tw',10136)
# ECB attack.
import urllib.parse
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
'''
1234567890123456
usr=OAOAO&admin=
N---------------

usr=OAOAOAOAOAOA
YOAOAOAOAOAOAOAO
OAOAOAOA&admin=N
----------------
'''
def pprint(s,n):
	for i in range(0,len(s),n):
		print(s[i:i+n])

	print()
usr1 = 'OAOAO'
usr2 = 'OAOAOAOAOAOAYOAOAOAOAOAOAOAOOAOAOAOA'
key = os.urandom(32)
aes = AES.new(key, AES.MODE_ECB)
token1 = urllib.parse.urlencode({'usr': 'OAOAO', 'admin': 'N'})
pprint(token1,16)
token1 = aes.encrypt(pad(token1.encode('utf8'))).hex()
pprint(token1,32)
token2 = urllib.parse.urlencode({'usr': 'OAOAOAOAOAOAYOAOAOAOAOAOAOAOOAOAOAOA', 'admin': 'N'})
pprint(token2,16)
token2 = aes.encrypt(pad(token2.encode('utf8'))).hex()
pprint(token2,32)

token = token1[:32]+token2[32:64]+token2[96:]
pprint(token,32)

token = unpad(aes.decrypt(bytes.fromhex(token))).decode('utf8')
print('decrypt!')
print(token)
token = urllib.parse.parse_qs(token)
print(token)
fk_token= 'usr=ABCDEFGHIJKLY23456789&admin=Y23456789&admin=N'
print(len(pad(fk_token.encode('utf8'))))
fk_token = aes.encrypt(pad(fk_token.encode('utf8'))).hex()
pprint(fk_token,32)

# print(token)
# print(token) : usr=OAO&admin=N
# construct admin = Y.

r = remote('csie.ctf.tw',10136)
r.send('1\n')
def reg(usr):
	r.sendlineafter('[>] ','register')
	r.sendlineafter('Username: ',usr)
	token = r.recvuntil('\n\n').strip().split(b' ')[2]
	return token
def log(token):
	r.sendlineafter('[>] ','login')
	r.sendlineafter('Token: ',token)
token1 = reg(usr1)
token2 = reg(usr2)
token = token1[:32]+token2[32:64]+token2[96:]
log(token)
# r.send('1\nregister\n'+usr1+'\nregister\n'+usr2+'\n')
r.interactive()
'''
source:

import urllib.parse
key = os.urandom(32)
aes = AES.new(key, AES.MODE_ECB)

if cmd == 'register':
    usr = input('[>] Username: ')
    token = urllib.parse.urlencode({'usr': usr, 'admin': 'N'})
    token = aes.encrypt(pad(token.encode('utf8'))).hex()
    print(f'[+] Token: {token}')

elif cmd == 'login':
    token = input('[>] Token: ')
    token = unpad(aes.decrypt(bytes.fromhex(token))).decode('utf8')
    token = urllib.parse.parse_qs(token)
    for k, vs in token.items():
        assert(len(vs) == 1)
        token[k] = vs[0]
    if token['admin'][0] == 'Y':
        print(f'[+] {flags[0]}')
    else:
        print(f'[!] Try harder')
    exit(0)
'''