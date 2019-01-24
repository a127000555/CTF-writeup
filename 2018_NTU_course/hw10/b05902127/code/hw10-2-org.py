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
def info():
    r.sendlineafter('> ','1')
    l = r.recvuntil('menu').split()
    # c,n,e
    return int(l[2]),int(l[8]),int(l[5])
def decrypt(c,i):
    # if i< 800:
        # return 0
    r.sendlineafter('> ','2')
    r.sendline(str(c))
    return int(r.recvuntil('menu').split()[2])%2

last_left = 0
last_right = pow(2,8*128)
while last_right-last_left > 5:
    r = remote('csie.ctf.tw',10140)
    # r = remote('localhost',12000)
    c,n,e= info()
    left,right = 0,n
    z = 2
    try:
        for i in range(1,1024):
            mid = (left+right)//2
            if mid < last_left :
                res = 1
            elif last_right < mid:
                res = 0
            else:
                res = decrypt(c * pow(z,i*e,n),i)
                print('f(2^{}*p) = {}'.format(i,bin(res)[2:].rjust(4,'0')))
            if res == 0:
                right = mid
            else:
                left = mid
            if (right-left) < 1:
                break
            print(str(left)[:20])
            # r.interaccdtive()
    except:
        pass
    last_left = left
    last_right = right
    print('now i:',i)
    print(long_to_bytes(left))

r.interactive()
