import os
import sys
import msgpack
import traceback
from Crypto.Cipher import AES


IV = os.urandom(16)
key = os.urandom(32)
def chunk(s, n):
    return [s[i:i+n] for i in range(0, len(s), n)]

def encrypt(s):
    size = len(s)
    assert(size >= 16)
    s = s + b'\x00' * (-size % 16)
    print('encrypt length: {}'.format(len(s)))
    aes = AES.new(key, AES.MODE_CBC, IV)
    enc = aes.encrypt(s)
    # print(' --- AES encrypt --- ')
    # pprint(enc.hex(),32)
    # print(' --- ----------- --- ')
    if len(enc) != size:
        blocks = chunk(enc, 16)
        blocks[-2], blocks[-1] = blocks[-1], blocks[-2]
        enc = b''.join(blocks)[:size]
    return enc


def decrypt(s):
    size = len(s)
    assert(size >= 16)
    if size % 16:
        blocks = chunk(s, 16)
        aes = AES.new(key, AES.MODE_ECB)
        tail = aes.decrypt(blocks[-2])[size % 16:]
        blocks[-2], blocks[-1] = blocks[-1] + tail, blocks[-2]
        s = b''.join(blocks)

    # print(' --- toAES decrypt --- ')
    # pprint(s.hex(),32)
    # print(' --- ----------- --- ')
    aes = AES.new(key, AES.MODE_CBC, IV)
    dec = aes.decrypt(s)
    return dec[:size]

def pprint(s,n,des=""):
    print('{:=^40s}'.format(des))
    print('len : {}'.format(len(s)))
    for i in range(0,len(s),n):
        print(s[i:i+n])
    print()
    print('{:=^40s}'.format(""))
def dump_token(usr,pwd):
	vc = os.urandom(20).hex()
	token = {'usr': usr, 'pwd': pwd, 'vc': vc}
	token = msgpack.dumps(token)
	return token
# \x83 start. len(key)- len(val) -len(key)- len(val) ..

'''
1234567890123456
-*usr*01234*pwd*
0123456789012345
678901234567*vc*
----------------
'''
'''
fake
token1 = dump_token(b'01234',b'0123456789012345678901234567')
print(token1[:16])
if token1[:16] != b'\x83\xa3usr\xa501234\xa3pwd\xbc':
	print('invalid')
	exit()
pprint(token1,16,' token1 ')
enc1 = encrypt(token1)
enc1 = enc1[:48]
print(enc1)
magic_bit =  bytes.fromhex(hex(enc1[31]^(0xda)^(0xa0))[2:])
print('magic',len(magic_bit))
enc2 = enc1[:31] + magic_bit + enc1[32:]
pprint(enc2,16,' enc2 ')
msg = decrypt(enc2)
pprint(msg,16,' msg ')
exit()
'''
'''
# local 
token1 = dump_token(b'a',b'bbbb')
token2 = dump_token(b'a',b'bbbb1234567890123456')
pprint(token1,16,' token1 ')
enc1 = encrypt(token1)
enc2 = encrypt(token2)
c1  = enc1[:16]
c1_2= enc2[:16]

fake_vc = b'\xa2vc\xac123456789012'
m3_xor_c1 = bytes.fromhex(hex(int(fake_vc.hex(),16)^int(c1.hex(),16)^int(c1_2.hex(),16))[2:])
token3 = dump_token(b'a',b'bbbb'+m3_xor_c1)
pprint(token3,16,' token2 ')
if token3[:16] != b'\x83\xa3usr\xa1a\xa3pwd\xb4bbbb':
	print('failed')
	exit()
enc3 = encrypt(token3)
c3 = enc3[16:32]
mix_c = c1+c3
msg = decrypt(mix_c)
print(msg)
msg = msgpack.loads(msg)
print(b'vc',msg[b'vc'])
'''
def login(usr,pwd):
	r.sendlineafter('[>] ','l')
	r.sendlineafter('Username: ',usr)
	r.sendlineafter('Password: ',pwd)
	m = r.recvuntil('\n\n')
	print(m)
	return bytes.fromhex(m.split(b'\n')[0].split(b' ')[2].decode())

from pwn import *
r = remote('csie.ctf.tw',10138)
# r = remote('localhost',12000)

enc1 = login(b'01234',b'0123456789012345678901234567')
enc1 = enc1[:48]
magic_bit =  bytes.fromhex(hex(enc1[31]^(0xda)^(0xa0))[2:])
enc2 = (enc1[:31] + magic_bit + enc1[32:]).hex()
print('token :',enc2)
r.send('v\n'+enc2+'\n\n')
# print(r.recv())
r.interactive()