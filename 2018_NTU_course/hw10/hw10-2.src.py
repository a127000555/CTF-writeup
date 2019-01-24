#!/usr/bin/env python3
import json
from Crypto.Util.number import *
import sys
# flag = open('flag', 'rb').read()
flag = b'evil cat attack!!'

flag = flag.ljust(128, b'\x00')

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
    print(f'm = {m}',file=sys.stderr)
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
    for _ in range(1024 // 4 + 5 + 10000):
        menu()
        cmd = input('> ')
        if cmd == '1':
            info(pub)
        elif cmd == '2':
            decrypt(pri)
        else:
            exit()

main()