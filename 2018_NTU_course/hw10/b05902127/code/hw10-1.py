#!/usr/bin/env python3
import json
from Crypto.Util.number import *
from gmpy2 import *
from random import randint
# import numpy as np
from TS import *
from crt import *
'''
# flag = open('flag', 'rb').read()
flag = b'evil cat attacks'
def genkey():
    while True:
        while True:
            p = 2
            while size(p) < 512:
                p *= getPrime(randint(2, 12))
            if isPrime(p + 1):
                p = p + 1
                break
        r = randint(100, 2 ** 512)
        q1, q2 = int(next_prime(r)), int(next_prime(3 * next_prime(r)))
        n, phi = p * q1 * q2, (p - 1) * (q1 - 1) * (q2 - 1)
        e = 4 * randint(10, 100)
        if GCD(e, phi) == 4:
            return (p, q1, q2, n, e)

p, q1, q2, n, e = genkey()
m = bytes_to_long(flag)
c = pow(m, e, n)
'''
n,e,c = json.load(open('data-1','r'))
def pollard(n):
    b,B = 2,2
    # b = B!
    while True:
        b = pow(b,B,n)
        res = GCD(n,b-1)
        if res != 1:
            return res
        B+=1
p = pollard(n)
print('p = ',p)
q1_m_q2 = n // p
print('q1_m_q2 = ',q1_m_q2)

# ref https://en.wikipedia.org/wiki/Fermat%27s_factorization_method
def FermatSieve(n):
    # Squares are always congruent to 0, 1, 4, 5, 9, 16 modulo 20
    n = n * 3
    print((3*n) % 20)
    filt1 = [0,1,4,5,9,16]
    filt2 = [ (x - n) % 20 for x in filt1]
    filt = lambda a: (a*a)%20 in filt1 and (a*a-n)%20 in filt2
    is_sqrt = lambda a: pow(int(sqrt(a)),2) == a
    now_a = isqrt(n)+1
    while True:
        print(now_a*now_a - n)
        if filt(now_a) and is_sqrt(now_a*now_a - n):
            a,b  = now_a, isqrt(now_a * now_a - n)
            return a+b , (a-b)//3
        now_a += 1
# print(sqrt(112))
# print(q1_m_q2)

q1, q2 = FermatSieve(q1_m_q2)
phi = (p - 1) * (q1 - 1) * (q2 - 1)
d = inverse(e//4, phi)
c = pow(c,d,n)

def dec(c, p,q):
    mp = TS(c,p)
    mq = TS(c,q)
    return [
        crt([mp, mq], [p, q]),
        crt([-mp, mq], [p, q]),
        crt([mp, -mq], [p, q]),
        crt([-mp, -mq], [p, q])]


for c2 in dec( c % q1_m_q2 , q1 , q2 ):
    for m in dec(c2 % q1_m_q2 , q1 , q2 ):
        # pass
        print(long_to_bytes(m))
# d = inverse(e, phi)
# m = pow(c, d, n)
