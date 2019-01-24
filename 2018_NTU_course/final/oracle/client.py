import json
# from pwn import *
from Crypto.Util.number import *
# server = remote('edu-ctf.zoolab.org',20000)

def info():
	server.sendlineafter('>',b"1")
	msg = server.recvlines(3)
	c = int(msg[0].split()[-1])
	e = int(msg[1].split()[-1])
	n = int(msg[2].split()[-1])
	return c,e,n

def decrypt(c):
	server.sendlineafter('>',b"2")
	server.sendlineafter('c = ',str(c))
	msg = int(server.recvlines(1)[0].split()[-1])
	return msg


def genkeys():
    e = 5
    while True:
        p, q = getPrime(512), getPrime(512)
        n, phi = p * q, (p - 1) * (q - 1)
        if GCD(e, phi) == 1:
            d = inverse(e, phi)
            return (n, e), (n, d)

(n,e) , (n,d) = genkeys()
print(bin(d)[2:].rjust(1024,'0'))

print(n-pow(n-1,d,n))
print(pow((n-1)//2,d,n)%2)
print(pow((n-1)//4,d,n)%2)
print(pow((n-1)//8,d,n)%2)

# c, e, n = info()
# print(math.log(n,2))
# for i in range(2,100000000):
# 	if n%i == 0:
# 		print(i)

# print('n',n)
# print(decrypt(2))
# print((decrypt(2)**2)%n)
# print(decrypt(4))
