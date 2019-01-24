import json
from Crypto.Util.number import *
from sage.all import *

prefix = b'evil cat'
suffix = b' attacks!'


def genkeys():
    e = 5
    while True:
        p, q = getPrime(512), getPrime(512)
        n, phi = p * q, (p - 1) * (q - 1)
        if GCD(e, phi) == 1:
            d = inverse(e, phi)
            return (n, e), (n, d)

def decrypt(pri,c):
    n, d = pri
    m = pow(c, d, n)
    return m 

def encrypt(pub,m):
    n, e = pub
    c = pow(m, e, n)
    return c

pub, pri = genkeys()
n, e = pub
m = bytes_to_long(prefix+suffix)
c = encrypt(pub,m)
prefix_n = bytes_to_long(prefix)
suffix_n = bytes_to_long(suffix)
# print(c,end='\n\n')
print(m,end='\n\n')
print(prefix_n,end='\n\n')
print(prefix_n*pow(256,len(suffix))+suffix_n)

print(c,end='\n\n')
print(
	encrypt(
		pub,prefix_n*pow(256,len(suffix))+
		suffix_n
	),end='\n\n')
print(
	(
		encrypt(pub,prefix_n*pow(256,len(suffix)))*
		encrypt(pub,suffix_n)
	)%n,end='\n\n')
exit()
for i in range(len(suffix),len(suffix)+1):
	remain = (c - encrypt(pub,prefix_n * pow(256,i))) % n 
	print(long_to_bytes(decrypt(pri,remain)))
	print(remain)
# print(long_to_bytes(decrypt(pri,c)))

'''
c = ( p*256^l + s )^ e
( p*256^l + s )^ e % n

(s^e) + (p*256^l) ^ e % n
'''