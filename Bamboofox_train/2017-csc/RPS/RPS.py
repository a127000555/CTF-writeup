
import random
from pwn import *
r = remote('bamboofox.cs.nctu.edu.tw',22004)
r.recvuntil("Let's play a game")
now = chr(r.recv()[0])
current = 0 if now == '!' else 1 if now == '?' else 2
play = ["rock","paper","scissors"]
hint = ['!','?',':']

for i in range(100):
	current = (current + 1) % 3
	r.sendline(play[current])
# print(random.randint(0,2))

r.interactive()