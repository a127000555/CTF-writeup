#!/usr/bin/env python3
import json
from Crypto.Util.number import *

# flag = open('flag', 'rb').read()
# flag = flag.ljust(128, b'\x00')

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
    print(f'c = {c}')
    print(f'e = {e}')
    print(f'n = {n}')

def decrypt(pri):
    n, d = pri
    c = int(input())
    m = pow(c, d, n)
    print(f'm = {m % (2 ** 4)}')

def main():
    pub, pri = genkeys()
    for _ in range(1024 // 4 + 5):
        menu()
        cmd = input('> ')
        if cmd == '1':
            info(pub)
        elif cmd == '2':
            decrypt(pri)
        else:
            exit()

# main()

from pwn import *
r = remote('csie.ctf.tw',10140)
def info():
    r.sendlineafter('> ','1')
    l = r.recvuntil('menu').split()
    # c,n,e
    return int(l[2]),int(l[8]),int(l[5])
def decrypt(c,i):
    r.sendlineafter('> ','2')
    r.sendline(str(c))
    return int(r.recvuntil('menu').split()[2])

c,n,e= info()
left,right = 0,n
z = 16
for i in range(1,1024):
    res = decrypt(c * pow(z,i*e,n),i)
    print('f(2^{}*p) = {}'.format(i,bin(res)[2:].rjust(4,'0')))
    left,right = left+(right-left)*res//z, left+(right-left)*(res+1)//z
    if (right-left) < 1:
        break
print(left,right)
print(long_to_bytes(left))

r.interactive()

