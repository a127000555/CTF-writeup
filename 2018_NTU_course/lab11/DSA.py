from hashlib import sha256
from pwn import *
from Crypto.PublicKey import DSA
from Crypto.Util.number import getRandomRange, long_to_bytes
from Crypto.Util.number import *

DSAkey = DSA.generate(1024)
q = DSAkey.q
k0 = 1
while pow(k0, (q - 1) // 2, q) != q - 1:
    k0 = getRandomRange(1, q)

k1 = pow(k0, 4, q)
k2 = pow(k0, q-4, q)
k3 = pow(k0, q, q)
# print(k1*k2 % q)
# print(k0)
# print(k3)

# exit()
def sign(msg):
	server.sendlineafter('Command: ',b'sign')
	server.sendlineafter('Message: ',msg)
	r = int(server.recvline().split()[2])
	s = int(server.recvline().split()[2])
	return r,s
def sha(s):
	if type(s) == type(1):
		return bytes_to_long(sha256(long_to_bytes(s)).digest())
	else:
		s = s.encode()
		return bytes_to_long(sha256(s).digest())

server = remote('csie.ctf.tw',10142)
# server = remote('localhost',10142)
_,_,p,_,_,q,_,_,g,_,_,y,_ = server.recvuntil('[>]').split()
p,q,g,y = int(p),int(q),int(g),int(y)
# exit()
# r.interactive()
m1 = hex( (q-1)//2 )[2:]
m2 = hex( 4 )[2:]
m3 = hex( q-4 )[2:]

r, s = sign(m1)
x = (( q-1 ) * s - sha((q-1)//2)) * inverse(r,q) % q

r2, s2 = sign(m2)
# s2 = k^-m2 ( sha(m2) + xr2 )
r3, s3 = sign(m3)
# s3 = k^-m3 ( sha(m3) + xr3 )
# s2 * s3 = k^-1 () ()
# k0 = (s2 * s3)^-1 () () 
k0 = (inverse(s2 * s3 , q) *  (sha(m2) + x*r2) * (sha(m3) + x*r3)) % q
MSG = b'GIMME THE FLAG !!!!!!!'
MSG = int.from_bytes(MSG, 'little') % q
print(x)
print(k0)
# assert pow(g,x,p) == y
# assert pow(k0,(q-1)//2,q) == q-1
k = pow(k0, MSG, q)
r = pow(g , k , p) % q
s = (inverse(k , q) * (sha(MSG) + x*r)) % q
server.sendline('flag')
server.sendline(str(r))
server.sendline(str(s))
server.interactive()