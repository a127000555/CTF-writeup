#!/usr/bin/env python3
import json 
from Crypto.Util.number import *

# flag = open('flag', 'rb').read()
flag = b'my name is m30w'
def genkeys():
    e = 65537
    while True:
        p, q = getPrime(512), getPrime(512)
        n, phi = p * q, (p - 1) * (q - 1)
        if GCD(e, phi) == 1:
            d = inverse(e, phi)
            return (n, e), (n, d)

def menu():
    print(f'{" menu ":=^20}')
    print('1) info')
    print('2) decrypt')

def info(pub):
    n, e = pub
    m = bytes_to_long(flag)
    c = pow(m, e, n)
    return c, n , e

def decrypt(pri,c):
    n, d = pri
    m = pow(c, d, n)
    return m % 2

def main():
    pub, pri = genkeys()
    while True:
        menu()
        cmd = input('> ')
        if cmd == '1':
            info(pub)
        elif cmd == '2':
            decrypt(pri)
        else:
            exit()
'''
pub, pri= genkeys()
c,n,e=info(pub)
m = bytes_to_long(flag)
l,r = 0,n
for i in range(1,1024):
    res = decrypt(pri, c * pow(2,i*e,n))
    print('f(2^{}*p) = {}'.format(i,res))
    mid = (l+r)//2
    if res == 0:
        r = mid
    else:
        l = mid
    if (r-l) < 1:
        break
'''
from pwn import *
r = remote('csie.ctf.tw',10139)
def info():
    r.sendlineafter('> ','1')
    l = r.recvuntil('menu').split()
    # c,n,e
    return int(l[2]),int(l[8]),int(l[5])
def decrypt(c,i):
    if i< 800:
        return 0
    r.sendlineafter('> ','2')
    r.sendline(str(c))
    return int(r.recvuntil('menu').split()[2])
c,n,e= info()
left,right = 0,n
for i in range(1,1024):
    res = decrypt(c * pow(2,i*e,n),i)
    print('f(2^{}*p) = {}'.format(i,res))
    mid = (left+right)//2
    if res == 0:
        right = mid
    else:
        left = mid
    if (right-left) < 1:
        break
    # r.interactive()

for i in range(left-20,right+20):
    print(long_to_bytes(i))

r.interactive()

