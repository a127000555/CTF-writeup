#!/usr/bin/env python3
import json
from Crypto.Util.number import *
flag = b'evil cat attacks'.ljust(20,b'\x00')

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
    return m % 16

print('m = {}'.format(bytes_to_long(flag)))
pub, pri = genkeys()
c,n,e = info(pub)
print(decrypt(pri,c))
