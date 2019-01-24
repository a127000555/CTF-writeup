#!/usr/bin/env python3
from Crypto.Util.number import *
import json

def readkey():
    return json.loads(open('key').read())

def init():
    n, e, d = readkey()
    m = bytes_to_long(open('flag', 'rb').read())
    c = pow(m, e, n)
    return n, e, d, c

def info(c, e, n):
    print(f'c = {c}')
    print(f'e = {e}')
    print(f'n = {n}')

def decrypt(c, d, n):
    cc = int(input('c = '))
    d = d & ((1 << (5 + size(n) // 2)) - 1)
    m = pow(cc, d, n)
    print(f'm = {m}')

def menu():
    print(f'{" menu ":=^20}')
    print('1) info')
    print('2) decrypt')

def main():
    n, e, d, c = init()
    while True:
        menu()
        cmd = input('> ')
        if cmd == '1':
            info(c, e, n)
        elif cmd == '2':
            decrypt(c, d, n)
        else:
            exit()

main()
