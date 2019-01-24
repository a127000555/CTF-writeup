from Crypto.PublicKey import RSA
from Crypto.Util.number import *
import pickle

b = 0x80036343727970746f2e5075626c69634b65792e5253410a5f5253416f626a0a7100298171017d71022858010000006571034a0100010058010000006e71048a1121cf5e9109eab827a8c9d015a82d1b900075622e
open('file1','wb').write(long_to_bytes(b))

f = open('file1','rb')
rsa_key = pickle.load(f)

print(rsa_key)
N = rsa_key.publickey().n
e = rsa_key.publickey().e

data = 0x8003431076698a4c959dbc8382948cb8e2bc5f5371008571012e
open('file2','wb').write(long_to_bytes(data))
bdata = pickle.load(open('file2','rb'))
C = bytes_to_long(bdata[0])

print('N =',N)
print('e =',e)
print('C =',C)

print(long_to_bytes(pow(data,e,N)))
print(long_to_bytes(data))

print(hex(N)[2:])
print(hex(data)[2:])
print(hex(bytes_to_long(b'BAMBOOFOX{123456789abcdef}'))[2:])
