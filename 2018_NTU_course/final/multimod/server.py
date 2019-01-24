#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import sys
import os
from Crypto.Util.number import getRandomInteger
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from phe import paillier


# Key generation
aeskey, aesiv = os.urandom(32), os.urandom(16)
rsa = RSA.generate(1024, e=65537)
ppub, ppri = paillier.generate_paillier_keypair(n_length=1024)
Ms = [getRandomInteger(1000) for _ in range(20)]
Ms = sorted(Ms)[::-1]


# Flags
with open('../private/flag.txt') as f:
    FLAG = f.read().strip()
token = os.urandom(Ms[-1].bit_length() // 8 - 1)
token = int.from_bytes(token, 'little')


# Crypto functions
def aesenc(m):
    aes = AES.new(aeskey, AES.MODE_CBC, aesiv)
    return aes.encrypt(m.to_bytes(2048 // 8, 'little')).hex()


def aesdec(m):
    aes = AES.new(aeskey, AES.MODE_CBC, aesiv)
    m = bytes.fromhex(m)
    assert(len(m) == 2048 // 8)
    return int.from_bytes(aes.decrypt(m), 'little')


def paienc(m):
    assert(m < ppub.n)
    m = ppub.raw_encrypt(m)
    return aesenc(m)


def paidec(m):
    m = aesdec(m)
    return ppri.raw_decrypt(m)


# Operations
def mul():
    A = aesdec(input("[>] What's wrong? "))
    B = aesdec(input("[>] Hmm... "))
    R = aesenc(A * B % ppub.nsquare)
    print(f'[+] The Force will be with you.')
    print(R)


def shredder(x):
    """
    Our special shredder to destroy the output when something bad happened :)
    (e.g. when plaintext >= Ms[-1])
    """
    for m in Ms:
        x = x % m
    return x


def POWEEERRR():
    palpatine = paidec(input('[>] Who are you? '))
    force = int(input('[>] How strong do you want to be? '))
    force = shredder(rsa.decrypt(force))
    palpatine = pow(palpatine, force, ppub.n)
    palpatine = paienc(palpatine)
    print('[+] POWAHHHHHHHHHHHH!!!!!!!!!!!!')
    print(palpatine)


def whoru():
    A = paidec(input('[>] Who are you? '))
    B = paidec(input('[>] Who am I? '))
    if A == B:
        print('[+] You were my brother, Anakin.')
    else:
        print('[+] No, I am your father.')


def main():
    print(f'[*] RSA Modulus: {rsa.n}')
    print(f'[*] Paillier N: {ppub.n}')
    # print(f'[*] DEBUG: {token}')
    print(f'[*] Token: {rsa.encrypt(token, None)[0]}')
    print(f'[*] One: {paienc(1)}')
    print(f'[*] Ms * {len(Ms)}:')
    for m in Ms:
        print(f'[|] {m}')

    for cnt in range(5000):
        cmd = input('[>] Command: ')
        if cmd == 'Abandoned me.':
            print('[+] Goodbye.')
            exit(0)
        elif cmd == 'Power! Unlimited power!':
            POWEEERRR()
        elif cmd == 'Help me!':
            mul()
        elif cmd == 'What happened?':
            whoru()
        elif cmd == str(token):
            print(f"[+] Oh, my dear friend. How I’ve missed you.")
            print(f'[+] Flag: {FLAG}')
            exit(0)
        else:
            print("[-] What a piece o' junk!")
            exit(0)
        # print(cnt, file=sys.stderr)
        print('')


if __name__ == '__main__':
    main()
